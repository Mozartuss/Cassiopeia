"""
    Module to send changing object positions through a pipe. Note that
    this is not a simulation, but a mockup.
"""
#
# Copyright (C) 2017  "Peter Roesch" <Peter.Roesch@fh-augsburg.de>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
# or open http://www.fsf.org/licensing/licenses/gpl.html
#
import sys
import time

from physics.calculation import Calculation
from rendering.simulation_constants import END_MESSAGE

__FPS = 60
__DELTA_ALPHA = 0.01


def startup(sim_pipe, json_path, delta_t, debug_mode=False):
    """
        Initialise and continuously update a position list.

        Results are sent through a pipe after each update step

        Args:
            :param delta_t:
            :param sim_pipe: (multiprocessing.Pipe): Pipe to send results
            :param debug_mode:
            :param json_path:
    """
    if debug_mode:
        try:
            import ptvsd
            ptvsd.enable_attach(address=("0.0.0.0", 5678))
            print("Physics waiting for debugger attach on port 5678")
            ptvsd.wait_for_attach()
            breakpoint()
        except ImportError:
            print("Please install the package 'ptvsd' in order to use debug-mode!")
            print("Example: pip install ptvsd")
    # set the dimensions according to our values
    # this will place the planets in our view-range
    # Rendering will scale the big Coordinates to fit into the -1/1-room
    calc = Calculation(json_path, delta_t)
    for frame in calc.calc_frame_positions():
        # Send the scale-factor, so that the positions are in viewport
        if frame.max() != 0:
            sim_pipe.send(1 / frame.max())
            # Send the positions of the frame
        sim_pipe.send(frame)
        if sim_pipe.poll():
            msg = sim_pipe.recv()
            if isinstance(msg, str) and msg == END_MESSAGE:
                print("Stopping calculations...")
                calc.stop()
        time.sleep(1 / __FPS)
    sys.exit(0)