from PIL import Image
import argparse
import random

STOP_CHAR = '$'

def str_to_bin(string):
  string += STOP_CHAR
  bin_arr = [format(ord(c), 'b') for c in string]
  for i in xrange(len(bin_arr)):
    diff = 7 - len(bin_arr[i])
    if diff > 0:
      bin_arr[i] = '0'*diff + bin_arr[i]

  return ''.join(bin_arr)


def bin_to_str(bin_str):
  step = 7
  string = ''
  for i in xrange(0, len(bin_str), step):
    ascii_str = bin_str[i:i + step]
    c = chr(int(ascii_str, 2))
    if c == STOP_CHAR:
      break

    string += c

  return string

def encode_pixel(pixel, char):
  if (pixel % 2 == 0 and char == '1') or (pixel % 2 == 1 and char == '0'):
    if pixel == 255:
      pixel -= 1
    elif pixel == 0:
      pixel += 1
    else:
      if random.random() < 0.5:
        pixel += 1
      else:
        pixel -= 1 

  return pixel


def encode(in_image, string):
  im = Image.open(in_image)
  pix = im.load()
  hight, width = im.size 

  encoded_str = str_to_bin(string)
  tmp_encoded_str = encoded_str + '0'*4

  str_count = 0
  exit_flag = False
  for i in xrange(hight):
    if exit_flag:
      break

    for j in xrange(width):
      pixel_arr = list(pix[i,j])
      for p in xrange(3):
        pixel_arr[p] = encode_pixel(pix[i,j][p], tmp_encoded_str[str_count + p])

      pix[i,j] = tuple(pixel_arr)
      
      str_count += 3
      if str_count >= len(encoded_str):
        exit_flag = True
        break

  out_image = in_image.split('.')[0] + '_out.' + in_image.split('.')[1]
  im.save(out_image)
  return out_image 

def decode(image):
  im = Image.open(image) 
  pix = im.load()
  hight, width = im.size 

  bin_str = ''
  for i in xrange(hight):
    for j in xrange(width):
      for p in xrange(3):
        bin_str += str(pix[i,j][p] % 2) 
        
  return bin_to_str(bin_str)


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='main')
  parser.add_argument('--img', type=str, default="Lenna.png",
  help='input image (default: Lenna.png)')
  parser.add_argument('--msg', type=str, help='message')
  parser.add_argument('--encode', action="store_true", help='encode message in image')
  parser.add_argument('--decode', action="store_true", help='decode message from image')

  args = parser.parse_args()
  if args.decode:
    print decode(args.img)

  if args.encode:
    out_file = encode(args.img, args.msg)
    print "encoded to {}".format(out_file)





