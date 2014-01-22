HEADER = '''#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:%s
#EXT-X-MEDIA-SEQUENCE:%s
'''

BODY = '''
#EXTINF:%s,
testIZZ3C3.ts'''

FOOTER = '''
EXT-X-ENDLIST'''

class M3U8:

    files = []
    target_duration = 10

    def add_file(file_name, file_length):
        files.append({'length': file_length, 'name': file_file})


    # Takes an M3U8 file as a string and adds all the contents to this object
    def render():
        render_head = HEADER % (self.target_duration, len(self.files))

        render_body = ''
        for f in files:
            render_body = render_body + '\n#EXTINF:' + f['length'] + '\n' + f['name']

        rendering = render_head + render_body + FOOTER

        return rendering

    # Takes an M3U8 file as a string and adds all the contents to this object
    def add_from_string(m3u8_body):
        lines = m3u8_body.split('\n')

        for count, line in enumerate(lines):
            if '#EXTINF:' in line:
                length = line.split('#EXTINF:')[1]
                name = lines[count + 1]

                have_file = next((item for item in files if item["name"] == name), None)
                if not have_file:
                    add_file(name, length)

