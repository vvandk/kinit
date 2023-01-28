import PIL.Image  # 安装依赖包：pip3 install pillow
from math import log
from SSIM_PIL import compare_ssim # 安装依赖包：pip3 install SSIM-PIL


def get_ssim_at_quality(photo, quality):
    """Return the ssim for this JPEG image saved at the specified quality"""
    ssim_photo = "tmp.jpg"
    # optimize is omitted here as it doesn't affect
    # quality but requires additional memory and cpu
    photo.save(ssim_photo, format="JPEG", quality=quality, progressive=True)
    ssim_score = compare_ssim(photo, PIL.Image.open(ssim_photo))
    return ssim_score


def _ssim_iteration_count(lo, hi):
    """Return the depth of the binary search tree for this range"""
    if lo >= hi:
        return 0
    else:
        return int(log(hi - lo, 2)) + 1


def jpeg_dynamic_quality(original_photo):
    """Return an integer representing the quality that this JPEG image should be
    saved at to attain the quality threshold specified for this photo class.

    Args:
        original_photo - a prepared PIL JPEG image (only JPEG is supported)
    """
    ssim_goal = 0.9 #the original value is 0.95
    hi = 35 #the original value is 85
    lo = 30 #the original value is 80

    # working on a smaller size image doesn't give worse results but is faster
    # changing this value requires updating the calculated thresholds
    photo = original_photo.resize((200, 200))

    # if not _should_use_dynamic_quality():
    #     default_ssim = get_ssim_at_quality(photo, hi)
    #     return hi, default_ssim

    # 95 is the highest useful value for JPEG. Higher values cause different behavior
    # Used to establish the image's intrinsic ssim without encoder artifacts
    normalized_ssim = get_ssim_at_quality(photo, 10)
    selected_quality = selected_ssim = None

    # loop bisection. ssim function increases monotonically so this will converge
    for i in range(_ssim_iteration_count(lo, hi)):
        curr_quality = (lo + hi) // 2
        curr_ssim = get_ssim_at_quality(photo, curr_quality)
        ssim_ratio = curr_ssim / normalized_ssim

        if ssim_ratio >= ssim_goal:
            # continue to check whether a lower quality level also exceeds the goal
            selected_quality = curr_quality
            selected_ssim = curr_ssim
            hi = curr_quality
        else:
            lo = curr_quality

    if selected_quality:
        return selected_quality, selected_ssim
    else:
        default_ssim = get_ssim_at_quality(photo, hi)
        return hi, default_ssim
