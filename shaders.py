import moderngl
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from array import array


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
display = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
ctx = moderngl.create_context()
# 'f' float-array
quad_buffer = ctx.buffer(data=array('f', [
    # position x, y, uv coords u, v
    # opengl coords for pos is -1:1 but ub is 0:1
    # everything is flipped on the y-axis because pygame has a flipped coord system compared to opengl
    -1.0, 1.0, 0.0, 0.0,     # top left
    1.0, 1.0, 1.0, 0.0,      # top right
    -1.0, -1.0, 0.0, 1.0,    # bottom left
    1.0, -1.0, 1.0, 1.0,     # bottom right
]))

# we use glsl to write the shader, usually this would be its own file
# TODO: make shader loader pipeline
    # out for uvs specified, but vert is set in main() with gl_Position
    # gl_Position refers to vertex, vec4(position x, y, z, mass/scale m) m is also called the homogones component
    # vert and vert.x, vert.y is equivalent here because vec2 gets squished into vec4 at position
vert_shader = '''
    # version 330 core
    
    in vec2 vert;
    in vec2 texcoord;
    out vec2 uvs;

    void main() {
        uvs = texcoord;
        gl_Position = vec4(vert, 0.0, 1.0);
    }
'''

    # uniform is a different kind of input as in
    # with texture() we build the rgb values from the sampled tex and uvs
frag_shader = '''
    # version 330 core
    
    uniform sampler2D tex;
    uniform float time;

    in vec2 uvs;
    out vec4 f_color;

    void main() {
        vec2 sample_pos = vec2(uvs.x + sin(uvs.y * 10 + time * 0.01) * 0.1, uvs.y);
        f_color = vec4(texture(tex, sample_pos).rg, texture(tex, sample_pos).b * 1.5, 1.0);
    }
'''

# shader program
program = ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
# ´2f 2f' is the format, and the for each we have to give it a label, matching the variables in the shader
render_object = ctx.vertex_array(program, [(quad_buffer, '2f 2f', 'vert', 'texcoord')])

def surf_to_texture(surf):
    tex = ctx.texture(surf.get_size(), 4)
    # interpolation, nearest is best with pixel art
    tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
    # pygame has a different channel sequence
    tex.swizzle = 'BGRA'
    # generates a surface
    tex.write(surf.get_view('1'))
    return tex




