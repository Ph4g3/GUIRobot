import sys

try:
    import test_Virtual_HID
except ImportError:
    print(sys.exc_info()[1])

test_Virtual_HID.main()
