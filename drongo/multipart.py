class File(object):
    def __init__(self, filename):
        self.filename = filename
        self.data = b''

        # FIXME: Write to a temporary file of memory

    def write(self, data):
        self.data += data

    def save_to(self, filename):
        with open(filename, 'wb') as fd:
            fd.write(self.data)

    def __repr__(self):
        return 'File(%s)' % self.filename


class Multipart(object):
    def __init__(self, boundary, length, input):
        self.boundary = boundary
        self.length = length
        self.input = input

    def readline(self):
        if self.length == 0:
            return b''

        data = self.input.readline()
        self.length -= len(data)
        return data

    def parse_header(self, header):
        header = header.split(';')
        result = {}
        for h in header:
            if '=' in h:
                k, v = h.split('=', 1)
                k = k.strip()
                v = v.strip()
                if v[0] == '"':
                    v = v[1:-1]
                result[k] = v
        return result

    def parse(self):
        boundary = self.boundary
        boundary1 = b'--' + boundary
        boundary2 = b'--' + boundary + b'--'
        result = {}

        first_line = self.readline()
        assert first_line.strip() == b'--' + boundary

        done = False

        while not done:
            headers = {}
            while True:  # read headers
                line = self.readline()
                if line == b'\r\n':
                    break

                if line.strip() == boundary1:
                    break
                elif line.strip() == boundary2:
                    done = True
                    break

                elif line.strip() == b'':
                    done = True
                    break

                line = line.decode('utf8')
                key, value = line.split(':')
                key = key.lower()
                value = value.strip()
                headers[key] = self.parse_header(value)

            if len(headers) == 0:
                continue

            # Read value
            if 'filename' not in headers['content-disposition']:
                line = self.readline()
                value = b''
                while not line.strip().startswith(boundary1):
                    value += line
                    line = self.readline()

                value = value.decode('utf8').strip()
                name = headers['content-disposition']['name']
                result.setdefault(name, []).append(value)
            else:
                ch = headers['content-disposition']
                name = ch['name']
                out = File(filename=ch['filename'])
                while self.length > 0:
                    line = self.readline()
                    if boundary in line:
                        break
                    out.write(line)
                if ch['filename']:
                    result.setdefault(name, []).append(out)

            if line.strip() == boundary2:
                done = True
                break

        return result
