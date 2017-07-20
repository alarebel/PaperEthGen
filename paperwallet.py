import os
import qrcode
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

print('Created by alarebel.')
print
print('Requires Python 2.7. Packages required: qrcode, pillow. To install, run the command "pip install qrcode pillow". If pip is not in your PATH, it is located int the Python27/Scripts/ folder.')
print
print('If running in shell window, right click the title bar->Properties and enable Quick Edit to paste into the window.')
print
print('This utility is intended to be used to create Ethereum Paper Wallets. For security reasons, wallet keys should be generated on an offline OS such as Ubuntu LiveCD and myetherwallet.com (downloaded from GitHub). Once a paper wallet is used, it is advised to immediately transfer unused funds in the paper wallet to a new paper wallet.')
print
print('Use this utility at your own risk. Code should be inspected for security issues before running. It is advised to run this script offline on Ubuntu LiveCD. The author of this utility cannot, in any way, be held responsible for any losses or damages.')

print
agree=raw_input('Do you agree with the above statement (y/n)? ')
if agree<>'y':
    exit()

print
filename=raw_input('Specify filename: (ie. out.pdf)')
if filename[-4:]<>'.pdf':
    filename=filename+'.pdf'

numwallets=raw_input('How many wallets will be created (3 max)? ')
numwallets=min(int(numwallets),3)

qrsize=300
dpi=300
dtext='0x4cdc8385e9f3247850c365225ecdaffe91d696e6'

#load background
background=Image.open('final.png','r')
bg_w, bg_h = background.size

#create page
page=Image.new('RGBA',(int(8.5*dpi),int(11*dpi)),(255,255,255,255))
pg_w, pg_h = page.size

for i in range(1,numwallets+1):
    #get address and pkey
    print
    print('Wallet: '+str(i))
    addtext=""
    pktext=""
    addtext=raw_input('Paste Address: ')
    
    if len(addtext)<1:
        print('Invalid address')
        exit()
    if addtext[0:2]<>'0x':
        addtext='0x'+addtext
            
    pktext=raw_input('Paste Private Key: ')
    if len(pktext)<1:
        print('Invalid private key')
        exit()
        
    #load addimg
    addimg = qrcode.make(addtext)
    add_w,add_h=addimg.size
    addimg=addimg.resize((qrsize,qrsize), Image.ANTIALIAS)
    add_w,add_h=addimg.size

    #load pkimg
    pkimg = qrcode.make(pktext)
    pk_w,pk_h=pkimg.size
    pkimg=pkimg.resize((qrsize,qrsize), Image.ANTIALIAS)
    pk_w,pk_h=pkimg.size

    #create new image
    img=Image.new('RGBA',(bg_w,bg_h),(255,255,255,255))
    img_w, img_h = img.size

    #paste background
    offset=(0,0)
    img.paste(background,offset)

    #paste addimg
    offset=(74,180)
    img.paste(addimg,offset)

    #paste pkimg
    img=img.rotate(180)
    offset=(74,180)
    img.paste(pkimg,offset)
    img=img.rotate(180)

    #add text
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('arial.ttf', 36)
    draw.text((85,40),addtext,(255,255,255),font=font)
    img=img.rotate(180)
    draw = ImageDraw.Draw(img)
    draw.text((85,40),pktext,(255,255,255),font=font)
    img=img.rotate(180)

    #Add to page
    offset=(int(pg_w/2 - bg_w/2),int(dpi/2)+(i-1)*(img_h+100))
    page.paste(img,offset)

page=page.convert('RGB')
page.save(filename,'PDF')

print
print('PDF saved as: '+filename)
dopen=raw_input('Open file now (y/n)? ')
if dopen=='y':
    os.startfile(filename)
print
print('Thanks for using this utility. Any donations are much appreciated:')
print(dtext)
e=raw_input('Press enter to exit or d and enter to display donation QRcode.')
if e=='d':
    dcode = qrcode.make(dtext)
    dcode.save('donation.png')
    os.startfile('donation.png')

