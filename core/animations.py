"""
 ============================================================
  MODULE/PLUGIN NAME: AnimationsEngine
  VERSION: 1.0.0
  MODULE CLASS: AnimationsEngine
  DESCRIPTION:
       Powerful terminal animation engine for visual effects

  AUTHOR:  Sebastian Januchowski
  COMPANY: polsoft.ITS™ Dev
  EMAIL:   polsoft.its@mail.com
  GITHUB:  polsoft-IT
  STATUS:  stable

 ============================================================
  COMPATIBILITY
 ============================================================
  PYTHON: 3.10+
  OS: Windows / Linux / macOS / Android (TerminalOS Runtime)
  ARCH: x86_64 / ARM64
  TERMINALOS KERNEL: v1.0+
"""

import time
import os
import random
import math
import asyncio
from typing import List, Callable, Dict, Optional


class AnimationsEngine:
    """Terminal animations engine with frame-based rendering"""
    
    def __init__(self):
        self.running = False
        self.current_animation = None
        self.stats = {
            'animations_played': 0,
            'total_frames': 0,
        }
        self.notification_callback = None
        
        # Built-in animations
        self.animations = {
            "matrix": self.anim_matrix,
            "fire": self.anim_fire,
            "wave": self.anim_wave,
            "spin": self.anim_spin,
            "pulse": self.anim_pulse,
        }
        
    def set_notification_callback(self, callback):
        """Set callback for animation notifications"""
        self.notification_callback = callback
        
    def clear(self):
        """Clear terminal screen"""
        os.system("cls" if os.name == "nt" else "clear")
        
    def play_frames(self, frames: List[str], delay: float = 0.05, repeat: bool = True) -> bool:
        """Play frame-based animation"""
        try:
            while self.running:
                for frame in frames:
                    if not self.running:
                        break
                    self.clear()
                    print(frame)
                    self.stats['total_frames'] += 1
                    time.sleep(delay)
                if not repeat:
                    break
            return True
        except KeyboardInterrupt:
            self.running = False
            return True
        except Exception as e:
            if self.notification_callback:
                self.notification_callback(
                    f"Animation error: {str(e)}",
                    "Frame playback failed",
                    "error",
                    "medium"
                )
            return False
            
    def anim_matrix(self, args: List[str] = None) -> bool:
        """Matrix rain animation"""
        width = 80
        height = 25
        chars = "01"
        self.running = True
        self.stats['animations_played'] += 1
        
        try:
            while self.running:
                self.clear()
                for _ in range(height):
                    line = "".join(random.choice(chars) for _ in range(width))
                    print(f"\033[38;2;0;255;0m{line}\033[0m")
                    self.stats['total_frames'] += 1
                time.sleep(0.05)
            return True
        except KeyboardInterrupt:
            self.running = False
            return True
        except Exception as e:
            if self.notification_callback:
                self.notification_callback(
                    f"Matrix animation error: {str(e)}",
                    "Animation failed",
                    "error",
                    "medium"
                )
            return False
            
    def anim_fire(self, args: List[str] = None) -> bool:
        """Fire ASCII animation"""
        width = 80
        height = 25
        self.running = True
        self.stats['animations_played'] += 1
        
        try:
            while self.running:
                self.clear()
                for y in range(height):
                    line = ""
                    for x in range(width):
                        r = random.randint(200, 255)
                        g = random.randint(50, 100)
                        b = random.randint(0, 20)
                        ch = random.choice(["█", "▓", "▒", "░"])
                        line += f"\033[38;2;{r};{g};{b}m{ch}"
                    print(line + "\033[0m")
                    self.stats['total_frames'] += 1
                time.sleep(0.05)
            return True
        except KeyboardInterrupt:
            self.running = False
            return True
        except Exception as e:
            if self.notification_callback:
                self.notification_callback(
                    f"Fire animation error: {str(e)}",
                    "Animation failed",
                    "error",
                    "medium"
                )
            return False
            
    def anim_wave(self, args: List[str] = None) -> bool:
        """Sine wave animation"""
        width = 80
        self.running = True
        self.stats['animations_played'] += 1
        
        try:
            t = 0
            while self.running:
                self.clear()
                for y in range(20):
                    line = ""
                    for x in range(width):
                        dy = int(5 * math.sin((x / 10) + t))
                        if y == 10 + dy:
                            line += "\033[36m~\033[0m"
                        else:
                            line += " "
                    print(line)
                    self.stats['total_frames'] += 1
                t += 0.2
                time.sleep(0.05)
            return True
        except KeyboardInterrupt:
            self.running = False
            return True
        except Exception as e:
            if self.notification_callback:
                self.notification_callback(
                    f"Wave animation error: {str(e)}",
                    "Animation failed",
                    "error",
                    "medium"
                )
            return False
            
    def anim_spin(self, args: List[str] = None) -> bool:
        """Spinner animation"""
        spinner_frames = ["|", "/", "-", "\\"]
        self.running = True
        self.stats['animations_played'] += 1
        
        try:
            while self.running:
                for frame in spinner_frames:
                    if not self.running:
                        break
                    self.clear()
                    print(f"Loading... {frame}")
                    self.stats['total_frames'] += 1
                    time.sleep(0.1)
            return True
        except KeyboardInterrupt:
            self.running = False
            return True
        except Exception as e:
            if self.notification_callback:
                self.notification_callback(
                    f"Spinner animation error: {str(e)}",
                    "Animation failed",
                    "error",
                    "medium"
                )
            return False
            
    def anim_pulse(self, args: List[str] = None) -> bool:
        """Pulsing text animation"""
        if not args:
            return False
            
        text = " ".join(args)
        self.running = True
        self.stats['animations_played'] += 1
        
        try:
            t = 0
            while self.running:
                self.clear()
                intensity = int((math.sin(t) + 1) * 127)
                print(f"\033[38;2;{intensity};0;{255-intensity}m{text}\033[0m")
                self.stats['total_frames'] += 1
                t += 0.2
                time.sleep(0.05)
            return True
        except KeyboardInterrupt:
            self.running = False
            return True
        except Exception as e:
            if self.notification_callback:
                self.notification_callback(
                    f"Pulse animation error: {str(e)}",
                    "Animation failed",
                    "error",
                    "medium"
                )
            return False
            
    def play(self, name: str, args: List[str] = None) -> bool:
        """Play animation by name"""
        if name in self.animations:
            return self.animations[name](args)
        return False
        
    def stop(self):
        """Stop current animation"""
        self.running = False
        
    def get_available_animations(self) -> List[str]:
        """Get list of available animations"""
        return list(self.animations.keys())
        
    def get_stats(self) -> Dict[str, any]:
        """Get animation engine statistics"""
        return {
            'animations_played': self.stats['animations_played'],
            'total_frames': self.stats['total_frames'],
            'available_animations': len(self.animations),
            'running': self.running,
        }
        
    def clear_stats(self):
        """Clear statistics"""
        self.stats = {
            'animations_played': 0,
            'total_frames': 0,
        }
        
    def add_custom_animation(self, name: str, func: Callable):
        """Add custom animation"""
        self.animations[name] = func
        
    def remove_animation(self, name: str) -> bool:
        """Remove custom animation"""
        if name in self.animations and name not in ["matrix", "fire", "wave", "spin", "pulse"]:
            del self.animations[name]
            return True
        return False


# Global instance
animations_engine = AnimationsEngine()
