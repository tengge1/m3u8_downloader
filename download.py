import os
import sys
import requests
import m3u8

# 下载合并文件


def download_file(url):
    try:
        r = requests.get(url, timeout=5)
        return r.content
    except:
        print(f'retry download.')
        return download_file(url)


def merge_files(name, segs):
    if os.path.exists(f'videos\\{name}.ts'):
        os.remove(f'videos\\{name}.ts')
    with open(f'videos\\{name}.ts', 'ab') as f:
        for i, seg in enumerate(segs):
            content = download_file(seg.uri)
            f.write(content)
            print(f'{name} seg {i} Done!')

# 解析m3u8文件


def parse_m3u8(url):
    m3u8_obj = m3u8.load(url)
    return m3u8_obj.segments

# 主函数


def download(name, url):
    files = parse_m3u8(url)
    merge_files(name, files)
    print(f'{name} Done!')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('需要3个参数')
        sys.exit(-1)
    if not sys.argv[2].startswith('http'):
        print('参数2需要以http开头')
        sys.exit(-1)
    if not sys.argv[2].endswith('m3u8'):
        print('参数2需要以m3u8结尾')
        sys.exit(-1)
    download(sys.argv[1], sys.argv[2])
