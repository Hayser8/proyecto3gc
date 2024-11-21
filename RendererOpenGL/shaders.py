
from xml.dom.expatbuilder import FragmentBuilder

vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;
out vec3 fragPos;  

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    vec4 worldPosition = modelMatrix * vec4(position, 1.0);
    fragPos = worldPosition.xyz;  
    gl_Position = projectionMatrix * viewMatrix * worldPosition;
    outTexCoords = texCoords;

    mat3 normalMatrix = transpose(inverse(mat3(modelMatrix)));
    outNormals = normalize(normalMatrix * normals);
}
'''

fragment_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;  

uniform sampler2D tex;

out vec4 fragColor;

void main()
{
    fragColor = texture(tex, outTexCoords);
}
'''

fat_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position + normals * sin(time * 3) / 10, 1.0); 
    outTexCoords = texCoords;
    outNormals = normals;
}
'''

water_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position + vec3(0,1,0) * sin(time * position.x * 10) / 10, 1.0); 
    outTexCoords = texCoords;
    outNormals = normals;
}
'''

wave = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    vec3 modifiedPosition = position;
    modifiedPosition.y += sin(position.x * 5.0 + time * 3.0) * 0.1; 
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(modifiedPosition, 1.0);
    outTexCoords = texCoords;
    outNormals = normals;
}
'''

pulse = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    float scale = 1.0 + 0.2 * sin(time * 2.0);
    vec3 modifiedPosition = position * scale;
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(modifiedPosition, 1.0);
    outTexCoords = texCoords;
    outNormals = normals;
}
'''

color = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;

uniform sampler2D tex;
uniform float time;

out vec4 fragColor;

void main()
{
    vec4 textureColor = texture(tex, outTexCoords);
    float red = 0.5 + 0.5 * sin(time + outTexCoords.x * 10.0);
    float green = 0.5 + 0.5 * sin(time + outTexCoords.y * 10.0);
    float blue = 0.5 + 0.5 * sin(time + outTexCoords.x * 10.0 + outTexCoords.y * 10.0);
    fragColor = vec4(textureColor.rgb * vec3(red, green, blue), textureColor.a);
}
'''

metallic = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;
in vec3 fragPos;

uniform sampler2D tex;
uniform vec3 lightPosition;
uniform vec3 cameraPosition;

out vec4 fragColor;

void main()
{
    vec3 norm = normalize(outNormals);
    vec3 lightDir = normalize(lightPosition - fragPos);
    float diff = max(dot(norm, lightDir), 0.0);

    vec3 viewDir = normalize(cameraPosition - fragPos);
    vec3 reflectDir = reflect(-lightDir, norm);

    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);

    vec4 textureColor = texture(tex, outTexCoords);
    vec3 finalColor = (textureColor.rgb * diff) + spec * vec3(1.0, 1.0, 1.0);

    fragColor = vec4(finalColor, textureColor.a);
}

'''

ripple = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    float ripple = sin(length(position.xy) * 5.0 - time * 5.0) * 0.1;
    vec3 modifiedPosition = position + normals * ripple;
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(modifiedPosition, 1.0);
    outTexCoords = texCoords;
    outNormals = normals;
}
'''

twist = ''' 
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    float twist = position.y * 0.5 + time; 
    vec3 modifiedPosition = vec3(
        position.x * cos(twist) - position.z * sin(twist),
        position.y,
        position.x * sin(twist) + position.z * cos(twist)
    );
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(modifiedPosition, 1.0);
    outTexCoords = texCoords;
    outNormals = normals;
}
'''

skybox_vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 inPosition;

uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

out vec3 texCoords;

void main()
{
    texCoords = inPosition;
    gl_Position = projectionMatrix * viewMatrix * vec4(inPosition, 1.0);
}
'''

skybox_fragment_shader = '''
#version 450 core

uniform samplerCube skybox;

in vec3 texCoords;

out vec4 fragColor;

void main()
{
    fragColor = texture(skybox, texCoords);
}
'''

po_shader_vertex = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    float scale = 1.0 + 0.02 * sin(time * 2.0);
    vec3 modifiedPosition = position * scale;
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(modifiedPosition, 1.0);
    outTexCoords = texCoords;
    outNormals = normals;
}
'''

tigress_fragment_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec3 fragPos;
in vec3 outNormals;

uniform sampler2D tex;
uniform vec3 lightPos;
uniform vec3 viewPos;

out vec4 fragColor;

void main()
{
    
    vec3 ambientColor = vec3(0.1, 0.1, 0.1); 
    float shininess = 32.0; 

    
    vec3 lightColor = vec3(1.0, 1.0, 1.0); 

    
    vec3 ambient = ambientColor * lightColor;

    
    vec3 norm = normalize(outNormals);
    vec3 lightDir = normalize(lightPos - fragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * lightColor;

    
    vec3 viewDir = normalize(viewPos - fragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), shininess);
    vec3 specular = spec * lightColor;

    
    vec4 textureColor = texture(tex, outTexCoords);

    
    vec3 result = (ambient + diffuse + specular) * textureColor.rgb;
    fragColor = vec4(result, textureColor.a);
}
'''

tigress_vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 fragPos;
out vec3 outNormals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    
    fragPos = vec3(modelMatrix * vec4(position, 1.0));
    
    
    outNormals = mat3(transpose(inverse(modelMatrix))) * normals;
    
    
    outTexCoords = texCoords;
    
    
    gl_Position = projectionMatrix * viewMatrix * vec4(fragPos, 1.0);
}

'''
monkey_shader_vertex = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    vec3 modifiedPosition = position;
    modifiedPosition.y += sin(position.x * 5.0 + time * 5.0) * 0.1;
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(modifiedPosition, 1.0);
    outTexCoords = texCoords;
    outNormals = normals;
}
'''

shifu_shader_fragment = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;

uniform sampler2D tex;
uniform float time;

out vec4 fragColor;

void main()
{
    vec4 textureColor = texture(tex, outTexCoords);

    float glow = sin(time * 2.0) * 0.5 + 0.5;
    vec3 glowColor = vec3(1.0, 0.9, 0.5) * glow;

    fragColor = vec4(textureColor.rgb + glowColor * 0.2, textureColor.a);
}
'''

bars_shader_fragment = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;

uniform sampler2D tex;
uniform float time;

out vec4 fragColor;

void main()
{
    vec4 textureColor = texture(tex, outTexCoords);
    float colorShift = sin(time * 2.0) * 0.5 + 0.5;
    fragColor = vec4(textureColor.rgb * colorShift, textureColor.a);
}
'''

punching_bag_shader_vertex = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    float angle = sin(time * 2.0) * 0.1;
    mat4 rotation = mat4(
        cos(angle), 0.0, sin(angle), 0.0,
        0.0,        1.0, 0.0,        0.0,
        -sin(angle),0.0, cos(angle), 0.0,
        0.0,        0.0, 0.0,        1.0
    );
    vec4 rotatedPosition = rotation * vec4(position, 1.0);
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * rotatedPosition;
    outTexCoords = texCoords;
    outNormals = mat3(rotation) * normals;
}
'''

bow_target_shader_fragment = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;

uniform sampler2D tex;
uniform float time;

out vec4 fragColor;

void main()
{
    vec2 center = vec2(0.5, 0.5);
    float distance = length(outTexCoords - center);
    float ripple = sin((distance * 20.0) - (time * 5.0));
    float intensity = 1.0 - (distance * 2.0);
    vec4 textureColor = texture(tex, outTexCoords);
    fragColor = textureColor * (0.5 + 0.5 * ripple * intensity);
}
'''

geometry_shader_bars = '''
#version 450 core

layout(triangles) in;
layout(triangle_strip, max_vertices = 6) out;

uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main() {
    
    for (int i = 0; i < 3; i++) {
        gl_Position = projectionMatrix * viewMatrix * gl_in[i].gl_Position;
        EmitVertex();
    }
    EndPrimitive();

   
    for (int i = 0; i < 3; i++) {
        vec4 scaledPos = gl_in[i].gl_Position * 1.2; 
        gl_Position = projectionMatrix * viewMatrix * scaledPos;
        EmitVertex();
    }
    EndPrimitive();
}

'''

bars_fragment_shader = '''
#version 450 core

in vec3 fragColor; 
out vec4 color;

void main() {
    color = vec4(fragColor, 1.0); 
}
'''
