"""
Start simulation and renderer in separate processes connected by a pipe.
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
import multiprocessing
import threading
import time
from signal import SIGINT, signal
from sys import argv, exit

from rendering import simulation_bridge, galaxy_renderer
from rendering.simulation_constants import END_MESSAGE


def _startup(json_path ="random_planets_x18.json", delta_t = 3600):
    currentthread = threading.currentThread()
    renderer_conn, simulation_conn = multiprocessing.Pipe()
    physics_debug_mode, render_debug_mode = False, False
    if len(argv) > 1:
        if argv[1] == "--debug-physics":
            physics_debug_mode = True
        elif argv[1] == "--debug-rendering":
            render_debug_mode = True

    simulation_process = \
        multiprocessing.Process(target=simulation_bridge.startup,
            args=(simulation_conn, json_path, delta_t, physics_debug_mode))

    render_process = \
        multiprocessing.Process(target=galaxy_renderer.startup,
            args=(renderer_conn, 60, render_debug_mode))

    simulation_process.start()
    render_process.start()

    while getattr(currentthread, "do_run", True):
        time.sleep(1)

    print("exit signal received")

    simulation_conn.send(END_MESSAGE)
    renderer_conn.send(END_MESSAGE)
    simulation_process.join()
    render_process.join()


if __name__ == '__main__':
    """
    json_path, delta_t
    """
    #_startup("random_planets_x18.json", 60 * 60)
