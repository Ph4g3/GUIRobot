import ctypes
import time
from ctypes.wintypes import (c_int, c_long, c_short, c_byte, c_ulong, c_ushort, 
                             POINT, POINTER, Structure, Union, sizeof, HHOOK,
                             HINSTANCE)

if __name__ == '__main__':
    run()
    
def run():
    
    global KeyBdHook
    global messages
    
    KeyBdHook = HHook()
    messages = []
        
    start = time.time()
    #Record keystrokes for 2 seconds.
    while time.time() < (start + 2):
        KeyBdHook.hook = SetWindowsHookEx(13, KeyboardProc,
                                          GetModuleHandle(0), 0)
        if KeyBdHook.hook == 0:
            print 'ERROR: '+str(ctypes.windll.kernel32.GetLastError())
        UnhookWindowsHookEx(KeyBdHook.hook)
        
    print messages
            
def KeyboardProc(nCode, wParam, lParam):
    """LLKeyboard procedure callback function for our hook to the OS.
    
       nCode tells us if we should pass an event onto the actual recipient 
       of the message first. We'll ignore this for now as we want to record
       all keystrokes.
       
       wParam gives us info on whether the key was pressed or released.
       
       lParam is a pointer to our KBLLSTRUCT.
       
       http://msdn.microsoft.com/en-us/library/ms644985(v=vs.85).aspx"""
      
    #nCode tells us if we should pass an event onto the actual recipient of the
    #message first. I say screw that - I want all the keystrokes first.
    if nCode < 0:
#            Keyboard event is passed through lParam, so copy this into our Python
#            KBDLLStruct type using a windows function 'MoveMemory'

       
        #Because it's a windows function calling this method, we'll want to
        #pass back information that we've taken so it can be used by other applications.
        return ctypes.windll.user32.GetNextHookEx(KeyBdHook.hook,
                                              nCode, wParam, lParam)
    else:
        ctypes.windll.kernel32.RtlMoveMemory(ctypes.addressof(KeyBdHook.kStruct),
                                             ctypes.c_void_p(lParam),
                                             ctypes.sizeof(lParam))
        
        messages.append(KeyBdHook.kStruct)
        return ctypes.windll.user32.GetNextHookEx(KeyBdHook.hook,
                                              nCode, wParam, lParam)
        #message.append(self.KeyBdHook.kStruct)

    
def SetWindowsHookEx(idHook, lpFn, hMod, dwThreadId):
    """Cast our python types into a Windows function type"""
    WinFunc = ctypes.WINFUNCTYPE(c_ulong, c_ulong, c_ulong, c_ulong)
    return ctypes.windll.user32.SetWindowsHookExA(idHook, WinFunc(lpFn), hMod, dwThreadId)

def GetModuleHandle(lpModuleName):
    return ctypes.windll.kernel32.GetModuleHandleA(lpModuleName)

def UnhookWindowsHookEx(hHook):
    return ctypes.windll.user32.UnhookWindowsHookEx(hHook)
    
class HHook():
    """A handle for the hook we use to get keyboard keystrokes."""
    
    def __init__(self):
        self.hook = HHOOK
        self.kStruct = KBLLHOOKSTRUCT()
        
class KBLLHOOKSTRUCT(Structure):
    """Holds information about keyboard events we receive from a hook procedure.
       Keyboard Low Level Hook Structure.
       http://msdn.microsoft.com/en-us/library/ms644967(v=vs.85).aspx"""
    
    #Kind of annoying how similar this is to the KeyBdInput Struct.
    _fields_ = [("vkCode", c_ulong),
                ("scanCode", c_ulong),
                ("flags", c_ulong),
                ("time", c_ulong),
                ("dwExtraInfo", POINTER(c_ulong))]