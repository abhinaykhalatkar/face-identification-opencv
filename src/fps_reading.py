class FPSCounter:
    def __init__(self):
        self.total_fps = 0.0  # Total FPS accumulated
        self.frame_count = 0  # Number of frames processed
        self.lowest_fps = float('inf')  # Initialize with a very high value
        self.highest_fps = 0.0  # Initialize with zero

    def update(self, fps):
        """Update the FPS counter with a new FPS value."""
        self.total_fps += fps
        self.frame_count += 1
        self.lowest_fps = min(self.lowest_fps, fps)
        self.highest_fps = max(self.highest_fps, fps)

    def get_average_fps(self):
        """Return the average FPS over all processed frames."""
        if self.frame_count == 0:
            return 0.0
        return self.total_fps / self.frame_count

    def get_lowest_fps(self):
        """Return the lowest FPS encountered."""
        return self.lowest_fps

    def get_highest_fps(self):
        """Return the highest FPS encountered."""
        return self.highest_fps

    def reset(self):
        """Reset the FPS counter."""
        self.total_fps = 0.0
        self.frame_count = 0
        self.lowest_fps = float('inf')
        self.highest_fps = 0.0
