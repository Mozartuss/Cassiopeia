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

from cassiopeia.rendering import simulation_bridge, galaxy_renderer
from cassiopeia.rendering.simulation_constants import END_MESSAGE
from signal import SIGINT, signal
from sys import argv, exit


def _startup():
    renderer_conn, simulation_conn = multiprocessing.Pipe()
    physics_debug_mode, render_debug_mode = False, False
    if len(argv) > 1:
        if argv[1] == "--debug-physics":
            physics_debug_mode = True
        elif argv[1] == "--debug-rendering":
            render_debug_mode = True
    simulation_process = \
        multiprocessing.Process(target=simulation_bridge.startup,
                                args=(simulation_conn, 16, 1, physics_debug_mode))
    render_process = \
        multiprocessing.Process(target=galaxy_renderer.startup,
                                args=(renderer_conn, 60, render_debug_mode))
    simulation_process.start()
    render_process.start()

    # Gets called on SIGINT (CTRL+C) and exits the program
    def handle_sigint(signum, x):
        print("Interrupt detected, simulation shutting down...")
        simulation_conn.send(END_MESSAGE)
        render_process.send(END_MESSAGE)
        simulation_process.join()  # Dunno what that does...
        render_process.join()
        render_process.terminate()  # Rendering needs to be killed explicitly
        exit(0)

    signal(SIGINT, handle_sigint)
    while True:
        pass


if __name__ == '__main__':
    _startup()
