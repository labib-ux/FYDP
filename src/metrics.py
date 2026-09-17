"""Audit metric harness: detection PR/F1/AP, mask IoU, regression errors.

Stdlib core (runs anywhere) + thin wrappers for sklearn/ultralytics when
installed. Covers the v1 gaps: no mAP, accuracy-only reporting, bbox-Ds
vs mask-Ds never compared, RF never ablated against Ds.

Self-test (no dependencies):
  python3 src/metrics.py --self-test
"""
import math
import sys

# --------------------------------------------------------------------------
# Boxes
# --------------------------------------------------------------------------

def bbox_iou(a, b):
    """IoU of two (x1, y1, x2, y2) boxes."""
    ix1, iy1 = max(a[0], b[0]), max(a[1], b[1])
    ix2, iy2 = min(a[2], b[2]), min(a[3], b[3])
    iw, ih = max(0.0, ix2 - ix1), max(0.0, iy2 - iy1)
    inter = iw * ih
    if inter <= 0:
        return 0.0
    area_a = max(0.0, a[2] - a[0]) * max(0.0, a[3] - a[1])
    area_b = max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1])
    union = area_a + area_b - inter
    return inter / union if union > 0 else 0.0


def _all_point_ap(scores, matched, n_gt):
    order = sorted(range(len(scores)), key=lambda i: -scores[i])
    tp = fp = 0
    precisions, recalls = [], []
    for i in order:
        if matched[i]:
            tp += 1
        else:
            fp += 1
        precisions.append(tp / (tp + fp))
        recalls.append(tp / n_gt if n_gt else 0.0)
    mrec = [0.0] + recalls + [1.0]
    mpre = [0.0] + precisions + [0.0]
    for i in range(len(mpre) - 2, -1, -1):
        mpre[i] = max(mpre[i], mpre[i + 1])
    ap = 0.0
    for i in range(len(mrec) - 1):
        if mrec[i + 1] != mrec[i]:
            ap += (mrec[i + 1] - mrec[i]) * mpre[i + 1]
    return ap


def detection_ap(preds, gts, iou_thr=0.5):
    """Mean AP over classes. preds: [(img, cls, score, bbox)], gts: [(img, cls, bbox)]."""
    classes = sorted({c for _, c, *_ in gts} | {c for _, c, *_ in preds})
    aps, detail = {}, {}
    for cls in classes:
        c_gts = [(img, box) for img, c, box in gts if c == cls]
        c_preds = [(img, s, box) for img, c, s, box in preds if c == cls]
        used = set()
        scores, matched = [], []
        # greedy match, score order
        for pi, (img, s, box) in enumerate(
                sorted(c_preds, key=lambda t: -t[1])):
            best, best_j = iou_thr, None
            for j, (gimg, gbox) in enumerate(c_gts):
                if gimg != img or j in used:
                    continue
                v = bbox_iou(box, gbox)
                if v >= best:
                    best, best_j = v, j
            scores.append(s)
            matched.append(best_j is not None)
            if best_j is not None:
                used.add(best_j)
        ap = _all_point_ap(scores, matched, len(c_gts))
        aps[cls] = ap
        detail[cls] = {"ap": ap, "n_gt": len(c_gts), "n_pred": len(c_preds)}
    mean_ap = sum(aps.values()) / len(aps) if aps else 0.0
    return mean_ap, detail


def detection_map_50_95(preds, gts):
    """mAP@.5 and mAP@.5:.95 (ten thresholds). Pure python; use for audit scale."""
    thrs = [round(0.5 + 0.05 * i, 2) for i in range(10)]
    per_thr = {}
    for t in thrs:
        m, _ = detection_ap(preds, gts, iou_thr=t)
        per_thr[t] = m
    return per_thr[0.5], sum(per_thr.values()) / len(per_thr), per_thr


# --------------------------------------------------------------------------
# Classification
# --------------------------------------------------------------------------

def confusion_prf(y_true, y_pred, labels=None):
    labels = labels or sorted(set(y_true) | set(y_pred))
    out = {}
    for lab in labels:
        tp = sum(1 for t, p in zip(y_true, y_pred) if t == lab and p == lab)
        fp = sum(1 for t, p in zip(y_true, y_pred) if t != lab and p == lab)
        fn = sum(1 for t, p in zip(y_true, y_pred) if t == lab and p != lab)
        prec = tp / (tp + fp) if (tp + fp) else 0.0
        rec = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0
        out[lab] = {"precision": prec, "recall": rec, "f1": f1,
                    "tp": tp, "fp": fp, "fn": fn}
    acc = (sum(1 for t, p in zip(y_true, y_pred) if t == p)
           / len(y_true) if y_true else 0.0)
    out["_accuracy"] = acc
    return out


# --------------------------------------------------------------------------
# Masks (bbox-Ds vs mask-Ds comparison)
# --------------------------------------------------------------------------

def mask_iou(mask_a, mask_b):
    """IoU of two binary masks given as nested sequences. Falls back to
    pure python so the audit runs without numpy; use numpy in prod."""
    try:
        import numpy as np
        a = np.asarray(mask_a, dtype=bool)
        b = np.asarray(mask_b, dtype=bool)
        inter = int((a & b).sum())
        union = int((a | b).sum())
        return inter / union if union else 1.0
    except ImportError:
        inter = union = 0
        for ra, rb in zip(mask_a, mask_b):
            for va, vb in zip(ra, rb):
                if va and vb:
                    inter += 1
                if va or vb:
                    union += 1
        return inter / union if union else 1.0


# --------------------------------------------------------------------------
# Regression (lead-time ablation: with-Ds vs without-Ds)
# --------------------------------------------------------------------------

def regression_metrics(y_true, y_pred):
    n = len(y_true)
    if not n:
        return {"mae": 0.0, "rmse": 0.0, "r2": 0.0, "n": 0}
    err = [t - p for t, p in zip(y_true, y_pred)]
    mae = sum(abs(e) for e in err) / n
    rmse = math.sqrt(sum(e * e for e in err) / n)
    mean_t = sum(y_true) / n
    ss_tot = sum((t - mean_t) ** 2 for t in y_true)
    ss_res = sum(e * e for e in err)
    r2 = 1 - ss_res / ss_tot if ss_tot else 0.0
    return {"mae": mae, "rmse": rmse, "r2": r2, "n": n}


# --------------------------------------------------------------------------
# Optional wrappers (need deps; fail with a clear message, not ImportError)
# --------------------------------------------------------------------------

def yolo_val(model_path, data_yaml, imgsz=640):
    try:
        from ultralytics import YOLO
    except ImportError:
        raise RuntimeError("ultralytics not installed — run: pip install -r requirements.txt")
    return YOLO(model_path).val(data=data_yaml, imgsz=imgsz)


def sklearn_prf(y_true, y_pred):
    try:
        from sklearn.metrics import precision_recall_fscore_support
    except ImportError:
        raise RuntimeError("scikit-learn not installed — run: pip install -r requirements.txt")
    labels = sorted(set(y_true) | set(y_pred))
    p, r, f, _ = precision_recall_fscore_support(y_true, y_pred, labels=labels,
                                                zero_division=0)
    return {lab: {"precision": float(p[i]), "recall": float(r[i]),
                  "f1": float(f[i])} for i, lab in enumerate(labels)}


# --------------------------------------------------------------------------
# Self-test
# --------------------------------------------------------------------------

def self_test():
    # boxes: perfect + partial + miss
    preds = [("im1", "hole", 0.9, (10, 10, 50, 50)),
             ("im1", "hole", 0.4, (200, 200, 210, 210)),
             ("im2", "stain", 0.8, (0, 0, 30, 30))]
    gts = [("im1", "hole", (10, 10, 50, 50)),
           ("im2", "stain", (0, 0, 30, 30))]
    m50, m5095, _ = detection_map_50_95(preds, gts)
    assert 0.5 <= m50 <= 1.0 and m5095 <= m50, (m50, m5095)
    assert abs(bbox_iou((0, 0, 10, 10), (0, 0, 10, 10)) - 1.0) < 1e-9
    assert bbox_iou((0, 0, 10, 10), (20, 20, 30, 30)) == 0.0
    prf = confusion_prf(["hole", "hole", "stain"], ["hole", "stain", "stain"])
    assert prf["_accuracy"] == 2 / 3
    assert mask_iou([[1, 0], [0, 1]], [[1, 0], [0, 1]]) == 1.0
    reg = regression_metrics([1.0, 2.0, 3.0], [1.0, 2.0, 3.0])
    assert reg["mae"] == 0.0 and reg["r2"] == 1.0
    print(f"self-test OK: mAP50={m50:.3f} mAP50-95={m5095:.3f} "
          f"acc={prf['_accuracy']:.3f} maskIoU=1.0 regR2=1.0")


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        self_test()
    else:
        print("usage: python3 src/metrics.py --self-test")
