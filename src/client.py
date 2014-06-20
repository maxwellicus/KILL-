#!/usr/bin/env python

# Copyright (C) 2011 by Xueqiao Xu <xueqiaoxu@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import sys
import time
import socket
import cPickle
import asyncore
import threading

import asynchatmod as asynchat

import pygame
from pygame.locals import *

from const.constants import *


# ==========================================================================
# Core
# ==========================================================================

class CoreClient(asynchat.async_chat, threading.Thread):
    """This is a hybrid class of asyn_chat and Thread. It deals with
    the communications with the server. An instance of this class
    will be a component of the Client and will be runned in a different
    thread apart from the GUI.
    """

    def __init__(self, address):
        """*Note*: the connection is established in the `run` routine 
        instead of __init__.
        """

        asynchat.async_chat.__init__(self)
        threading.Thread.__init__(self)

        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = address

        self.set_terminator(TERM)

        # incomming data buffer
        self.data = []

        # command dictionary, dispatches the command from the server
        self.cmd_dict = {'OPEN': self._cmd_open,
                         'CLOSE': self._cmd_close,
                         'VALUE': self._cmd_value,
                         'PARENT': self._cmd_parent,
                         'PATH': self._cmd_path}

        # algorithm dictionary
        self.algo_dict = {ASTARM: 'ASTARM',
                          ASTARE: 'ASTARE',
                          ASTARC: 'ASTARC',
                          DIJKSTRA: 'DIJKSTRA',
                          BDBFS: 'BDBFS'}

    def run(self):
        """Overides the run method of threading.Thread
        """

        # try to connect the server every COUNTDOWN_COOLDOWN seconds 
        # if not connected
        while not self.connected:
            try:
                self.connect(self.server_address)
            except Exception, e:
                print 'Unable to connect', self.server_address
                print 'Retry in %d seconds' % COUNTDOWN_COOLDOWN
                time.sleep(COUNTDOWN_COOLDOWN)

                self.close()
                self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
                
        print 'connected with server at', self.server_address
        
        # begin the main loop
        try:
            asyncore.loop()
        except KeyboardInterrupt:
            self.close()
            raise SystemExit


    def collect_incoming_data(self, data):
        self.data.append(data)

    def found_terminator(self):
        try:
            cmd, arg = cPickle.loads(''.join(self.data))
            self.cmd_dict[cmd](arg)
        except (ValueError,cPickle.UnpicklingError, LookupError), e:
            print e
        finally:
            self.data = []

    def calc(self, str_map, algo, speed):
        """Request for starting the calculation.
        """
        data_algo = cPickle.dumps(('ALGO', self.algo_dict[algo])) + TERM
        data_map = cPickle.dumps(('MAP', str_map)) + TERM
        data_speed = cPickle.dumps(('SPEED', speed)) + TERM
        data_start = cPickle.dumps(('START', '')) + TERM

        self.push(data_algo)
        self.push(data_map)
        self.push(data_speed)
        self.push(data_start)


    def toggle_speed(self, speed):
        data_speed = cPickle.dumps(('SPEED', speed)) + TERM
        self.push(data_speed)
    
    def stop(self):
        data_stop = cPickle.dumps(('STOP', '')) + TERM
        self.push(data_stop)

    def set_open_callback(self, callback):
        self.open_callback = callback

    def set_close_callback(self, callback):
        self.close_callback = callback

    def set_value_callback(self, callback):
        self.value_callback = callback

    def set_parent_callback(self, callback):
        self.parent_callback = callback

    def set_path_callback(self, callback):
        self.path_callback = callback

    def _cmd_open(self, arg):
        self.open_callback(arg, OPENED)

    def _cmd_close(self, arg):
        self.close_callback(arg, CLOSED)

    def _cmd_value(self, arg):
        which, pos, val = arg
        self.value_callback(pos, which, val)
        
    def _cmd_parent(self, arg):
        pos1, pos2 = arg
        self.parent_callback(pos1, pos2)

    def _cmd_path(self, arg):
        self.path_callback(arg)

    


# ======================================================================
# GUI 
# ======================================================================



class _Node(object):
    def __init__(self, (x, y)):
        self.pos = x, y
        left = x * NODE_SIZE
        top = y * NODE_SIZE
        self.rect = Rect(left, top, NODE_SIZE, NODE_SIZE)
        self.status = NORMAL
        self.parent = None
        self.f = None
        self.g = None
        self.h = None




class _HelpInfo(object):
    """Help info on the top left of the window.
    """
    def __init__(self, ui_path):
        """
        :Parameters:
            ui_path : str
                the folder where the ui resources are located
        """
        self.pos = HELP_POS
        self.text_pos = HELP_TEXT_POS
        self.background = pygame.image.load(
                os.path.join(ui_path, 'layer1.png')).convert_alpha()
        self.text = ("Drag Green and Red block to set source and target",
                     "Hold down mouse button to draw maze",
                     "Press <W> and <S> to select algorithm",
                     "Press <A> and <D> to set demo speed",
                     "Press <SPACE> to start or stop demo",
                     "Press <R> to reset")

        self.font = pygame.font.Font(os.path.join(
            ui_path, FONT_NAME), HELP_FONT_SIZE)
        self.img = [self.font.render(line, True, Color(HELP_FONT_COLOR)) 
                for line in self.text]

    def draw(self, surface):
        surface.blit(self.background, self.pos)
        x, y = self.text_pos
        for img in self.img:
            surface.blit(img, (x, y))
            y += HELP_Y_OFFSET




class _ControlInfo(object):

    def __init__(self, ui_path, core):
        """
        :Parameters:
            ui_path : str
                the folder where the ui resources are located

            core : async_chat
                the core client
        """
        self.pos = CONTROL_POS
        self.background = pygame.image.load(
                os.path.join(ui_path, 'layer2.png')).convert_alpha()
        self.text_pos = CONTROL_TEXT_POS
        self.algo_text = ('A* (Manhattan)',
                          'A* (Euclidean)',
                          'A* (Chebyshev)',
                          'Dijkstra',
                          'Bi-Directional BFS')
        self.selection = 0
        self.speed_text = 'Speed : '
        self.speed = DEFAULT_SPEED

        self.font = pygame.font.Font(os.path.join(
            ui_path, FONT_NAME), CONTROL_FONT_SIZE)
        self.algo_text_img = [self.font.render(line, True,
            Color(CONTROL_FONT_COLOR)) for line in self.algo_text]
        self.algo_selected_img = [self.font.render(line, True,
            Color(SELECTED_COLOR)) for line in self.algo_text]
        self.speed_img = self.font.render(self.speed_text, True,
            Color(SPEED_FONT_COLOR))

        self.core = core
    
    def draw(self, surface):
        # draw background
        surface.blit(self.background, self.pos)
        
        # draw algorithm text
        x, y = self.text_pos
        for i in xrange(len(self.algo_text_img)):
            if i == self.selection:
                surface.blit(self.algo_selected_img[i], (x, y))
            else:
                surface.blit(self.algo_text_img[i], (x, y))
            y += CONTROL_Y_OFFSET
        
        # draw speed text
        surface.blit(self.speed_img, (x, y))
        speed_img = self.font.render(str(self.speed) + ' X', True,
            Color(SELECTED_COLOR))
        x += self.speed_img.get_width()
        surface.blit(speed_img, (x, y))


    def toggle_selection(self, val):
        self.selection = (self.selection + val) % len(self.algo_text)

    def toggle_speed(self, val):
        speed = int(self.speed * (2 ** val))
        if speed >= 1 and speed <= SPEED_MAX:
            self.speed = speed

            # send the server the new speed
            self.core.toggle_speed(self.speed)




class _ConnectionInfo(object):

    def __init__(self, ui_path, core):
        """
        :Parameters:
            ui_path : str
                the folder where the ui resources are located

            core : async_chat
                the core client
        """
        self.ui_path = ui_path
        self.core = core

        # failure text
        self.failure_text = "Unable to connect to server at %s" % \
                str(core.server_address)
        self.failure_font = pygame.font.Font(
                os.path.join(self.ui_path, FONT_NAME),
                CONNECTION_FAILURE_FONT_SIZE)
        self.failure_img = self.failure_font.render(self.failure_text, True,
                Color(CONNECTION_FAILURE_COLOR))

        # countdown text
        self.countdown_font = pygame.font.Font(
                os.path.join(self.ui_path, FONT_NAME), 
                CONNECTION_COUNTDOWN_FONT_SIZE)

        self.countdown = COUNTDOWN_COOLDOWN
        self.countframe = self.countdown * FPS_LIMIT

        self.caption_changed = False


    def draw(self, surface):
        if self.core.connected:
            if not self.caption_changed:
                pygame.display.set_caption("%s   Connected to server at %s" % 
                        (CAPTION, self.core.server_address))
                self.caption_changed = True
        else:
            # draw failure text
            failure_pos = ((RESOLUTION[0] - self.failure_img.get_width()) / 2,
                           CONNECTION_FAILURE_Y)
            surface.blit(self.failure_img, failure_pos)
            
            # update counter
            self.countframe -= 1
            self.countdown = int(self.countframe / FPS_LIMIT) + 1
            if self.countframe == 0:
                self.countframe = COUNTDOWN_COOLDOWN * FPS_LIMIT
            
            # draw countdown text
            countdown_text = "Retry to connect in %d seconds" % self.countdown
            countdown_img = self.countdown_font.render(countdown_text, True,
                    Color(CONNECTION_FAILURE_COLOR))
            countdown_pos = ((RESOLUTION[0] - countdown_img.get_width()) / 2,
                            CONNECTION_COUNTDOWN_Y)
            surface.blit(countdown_img, countdown_pos)





class Client(object):
    
    def __init__(self, ui_path, addr):

        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()

        # core client, deals with the communications.
        self.core = CoreClient(addr)
        self.core.set_open_callback(self._set_node_status)
        self.core.set_close_callback(self._set_node_status)
        self.core.set_value_callback(self._set_node_value)
        self.core.set_parent_callback(self._set_node_parent)
        self.core.set_path_callback(self._set_path)
        self.core.setDaemon(True)

        # GUI related stuffs
        pygame.display.set_icon(
                pygame.image.load(os.path.join(ui_path, ICON_NAME)))
        self.screen = pygame.display.set_mode(RESOLUTION)
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()

        self.map_size = MAP_SIZE
        self.map_width, self.map_height = MAP_SIZE
        self.n_col = int(self.map_width / NODE_SIZE)
        self.n_row = int(self.map_height / NODE_SIZE)
        
        # builds nodes map
        self.nodes = [[_Node((x, y)) 
            for x in xrange(self.n_col)] 
                for y in xrange(self.n_row)]

        # color dictionary
        self.node_color = {NORMAL: Color(NORMAL_COLOR),
                           BLOCKED: Color(BLOCKED_COLOR),
                           OPENED: Color(OPENED_COLOR),
                           CLOSED: Color(CLOSED_COLOR),
                           SOURCE: Color(SOURCE_COLOR),
                           TARGET: Color(TARGET_COLOR)}

        self.node_font = pygame.font.Font(os.path.join(
            ui_path, FONT_NAME), NODE_INFO_FONT_SIZE)
        
        # floating texts
        self.control_info = _ControlInfo(ui_path, self.core)
        self.help_info = _HelpInfo(ui_path)
        self.connection_info = _ConnectionInfo(ui_path, self.core)

        
        self.source = (3, 9)
        self.target = (22, 9)
        self.path = []

        # general status
        self.status = DRAWING
        self.editable = False
        self.erasing = False
        self.drag = None


    def run(self):
        """Starts the main loop
        """
        self.core.start()

        # handle events
        while self.status != EXIT:

            for event in pygame.event.get():
                if event.type == QUIT:
                    self._quit()
                elif event.type in (MOUSEMOTION, 
                                    MOUSEBUTTONDOWN,
                                    MOUSEBUTTONUP):
                    self._handle_mouse(event)
                elif event.type == KEYDOWN:
                    self._handle_keyboard(event)
            
            # draw stuffs
            self._draw_background()
            self._draw_nodes()
            self._draw_source_target()
            self._draw_parent_lines()
            self._draw_grid_lines()
            self._draw_path()
            self.control_info.draw(self.screen)
            self.help_info.draw(self.screen)
            self.connection_info.draw(self.screen)

            # update screen
            pygame.display.update()

            # control frame rate
            self.clock.tick(FPS_LIMIT)


    def _quit(self):
        """Initiate termination
        """
        pygame.quit()
        self.core.close()
        raise SystemExit


    def _handle_mouse(self, event):
        """Handle mouse events.
        """
        x, y = event.pos 
        nx, ny = int(x / NODE_SIZE), int(y / NODE_SIZE)

        if event.type == MOUSEBUTTONDOWN:
            # if mouse pointer is on either source or target nodes,
            # then drag them around.
            if (nx, ny) == self.source:
                self.drag = SOURCE
            elif (nx, ny) == self.target:
                self.drag = TARGET
            else:
                # if mouse pointer is on BLOCKED nodes,
                # then set the following operations to be erasing
                # otherwise set to be blocking
                self.editable = True
                if self.nodes[ny][nx].status == BLOCKED:
                    self.erasing = True
                elif self.nodes[ny][nx].status != BLOCKED:
                    self.erasing = False

        elif event.type == MOUSEBUTTONUP:
            self.editable = False
            self.drag = None

        # toggle BLOCKED / NORAML status
        if self.editable:
            if self.erasing == True:
                self._set_node_status((nx, ny), NORMAL)
            else:
                self._set_node_status((nx, ny), BLOCKED)
        
        # drag source or target node
        if self.drag == SOURCE:
            self.source = nx, ny
        elif self.drag == TARGET:
            self.target = nx, ny


    def _handle_keyboard(self, event):
        """Handle keyboard events
        """
        if event.key == K_w:
            self.control_info.toggle_selection(-1)
        elif event.key == K_s:
            self.control_info.toggle_selection(1)
        elif event.key == K_d:
            self.control_info.toggle_speed(1)
        elif event.key == K_a:
            self.control_info.toggle_speed(-1)
        elif event.key == K_SPACE and self.core.connected:
            # starts computation
            if self.status == DRAWING:
                self._reset_except_block()
                self.status = RECEIVING
                self.core.calc(self._get_str_map(), 
                        self.control_info.selection,
                        self.control_info.speed)
            elif self.status == RECEIVING:
                self.status = DRAWING
                self.core.stop()
        elif event.key == K_r:
            self._reset()
        elif event.key == K_ESCAPE:
            self.quit()

    def _set_node_status(self, (x, y), status):
        try:
            self.nodes[y][x].status = status
        except LookupError, why:
            print why

    def _set_node_value(self, (x, y), which, val):
        try:
            setattr(self.nodes[y][x], which, val)
        except AttributeError, why:
            print why

    def _set_node_parent(self, (x1, y1), (x2, y2)):
        try:
            self.nodes[y1][x1].parent = self.nodes[y2][x2]
        except LookupError, why:
            print why

    def _set_path(self, path):
        self.status = DRAWING
        self.path = path

    def _draw_background(self):
        self.screen.fill(Color(BACKGROUND_COLOR))

    def _draw_nodes(self):
        for row in self.nodes:
            for node in row:
                self._draw_node_rect(node)
                self._draw_node_info(node)

    def _draw_node_rect(self, node):
        try:
            pygame.draw.rect(self.screen, self.node_color[node.status], 
                    node.rect, 0)
        except LookupError:
            pass


    def _draw_source_target(self):
        """Source and target nodes are drawed on top of other nodes.
        """
        x, y = self.source
        nx, ny = x * NODE_SIZE, y * NODE_SIZE
        pygame.draw.rect(self.screen, self.node_color[SOURCE], 
                Rect(nx, ny, NODE_SIZE, NODE_SIZE)) 

        x, y = self.target
        nx, ny = x * NODE_SIZE, y * NODE_SIZE
        pygame.draw.rect(self.screen, self.node_color[TARGET], 
                Rect(nx, ny, NODE_SIZE, NODE_SIZE)) 

        
    def _draw_node_info(self, node):
        if node.f:
            img = self.node_font.render(str(node.f), True,
                    Color(NODE_INFO_COLOR))
            x = node.rect.left + MARGIN
            y = node.rect.top + MARGIN
            self.screen.blit(img, (x, y))
        if node.g:
            img = self.node_font.render(str(node.g), True,
                    Color(NODE_INFO_COLOR))
            x = node.rect.left + MARGIN
            y = node.rect.bottom - img.get_height() - MARGIN + 1
            self.screen.blit(img, (x, y))
        if node.h:
            img = self.node_font.render(str(node.h), True,
                    Color(NODE_INFO_COLOR))
            x = node.rect.right - img.get_width() - MARGIN + 1
            y = node.rect.bottom - img.get_height() - MARGIN + 1
            self.screen.blit(img, (x, y))
                
    def _draw_parent_lines(self):
        for row in self.nodes:
            for node in row:
                if node.parent:
                    pygame.draw.line(self.screen, 
                        Color(PARENT_LINE_COLOR),
                        node.parent.rect.center, node.rect.center, 1)


    def _draw_grid_lines(self):
        for x in xrange(0, self.map_width, NODE_SIZE):
            pygame.draw.line(self.screen, Color(GRID_LINE_COLOR),
                    (x, 0), (x, self.map_height), 1)
        for y in xrange(0, self.map_height, NODE_SIZE):
            pygame.draw.line(self.screen, Color(GRID_LINE_COLOR),
                    (0, y), (self.map_width, y), 1)

    def _draw_path(self):
        if self.path:
            self.status = DRAWING
            seg = [self.nodes[y][x].rect.center 
                    for (x, y) in self.path]
            pygame.draw.lines(self.screen, Color(PATH_COLOR), False,
                    seg, PATH_WIDTH)


    def _reset(self):
        """Reset all nodes to be NORMAL and clear the node infos
        """
        self.path = []
        for row in self.nodes:
            for node in row:
                node.status = NORMAL
                node.f = None
                node.g = None
                node.h = None
                node.parent = None

    def _reset_except_block(self):
        """Same as _reset, but does not clear the blocked nodes
        """
        self.path = []
        for row in self.nodes:
            for node in row:
                if node.status != BLOCKED:
                    node.status = NORMAL
                node.f = None
                node.g = None
                node.h = None
                node.parent = None

    def _get_str_map(self):
        """Generate a string represented map from the current nodes' status.
        """
        final_str = []
        for row in self.nodes:
            str = []
            for node in row:
                if node.pos == self.source:
                    str.append(SOURCE)
                elif node.pos == self.target:
                    str.append(TARGET)
                else: 
                    str.append(node.status)
            str.append('\n')
            final_str.append(''.join(str))
        return ''.join(final_str)


def print_help():
    print """Usage: client.py [-a address] [-p port]
Example: client.py -a 172.18.241.2 -p 31416

The default address and port is localhost:31416
          """


if __name__ == '__main__':
    host = 'localhost'
    port = 31416

    import getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'ha:p:', ['help'])
        for o, a in opts:
            if o in ('-h', '--help'):
                print_help()
                raise SystemExit
            elif o == '-a':
                address = a
            elif o == '-p':
                port = int(a)

    except (getopt.GetoptError, ValueError):
        print 'Invalid arguments\n'
        print_help()
        raise SystemExit
    cur_path = os.path.abspath(os.path.dirname(__file__))
    ui_path = os.path.join(cur_path, 'ui')

    client = Client(ui_path, (host, port))
    client.run()
