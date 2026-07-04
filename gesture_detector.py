def finger_is_up(tip, pip, hand):
    return hand[tip].y < hand[pip].y


def finger_is_down(tip, pip, hand):
    return hand[tip].y > hand[pip].y


def detect_gesture(hand):

    thumb = hand[4]
    thumb_ip = hand[3]

    thumb_up = thumb.y < thumb_ip.y

    index_up = finger_is_up(8, 6, hand)
    middle_up = finger_is_up(12, 10, hand)
    ring_up = finger_is_up(16, 14, hand)
    pinky_up = finger_is_up(20, 18, hand)

    index_down = finger_is_down(8, 6, hand)
    middle_down = finger_is_down(12, 10, hand)
    ring_down = finger_is_down(16, 14, hand)
    pinky_down = finger_is_down(20, 18, hand)

    # 👍
    if thumb_up and index_down and middle_down and ring_down and pinky_down:
        return "THUMBS UP"

    # ✋
    if thumb_up and index_up and middle_up and ring_up and pinky_up:
        return "OPEN PALM"

    # 👊
    if index_down and middle_down and ring_down and pinky_down:
        return "FIST"

    return "UNKNOWN"