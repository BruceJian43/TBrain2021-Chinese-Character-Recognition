# https://data.gov.tw/dataset/5961
wget https://www.cns11643.gov.tw/AIDB/Open_Data.zip
unzip -q Open_Data.zip
mkdir TW-Kai
# 只拿楷體
mv Open_Data/Fonts/TW-Kai-98_1.ttf TW-Kai/
mv Open_Data/Fonts/TW-Kai-Plus-98_1.ttf TW-Kai/

# jasonhandwriting
git clone https://github.com/jasonhandwriting/JasonHandwriting.git

# https://github.com/ButTaiwan
git clone https://github.com/ButTaiwan/genyo-font.git
git clone https://github.com/ButTaiwan/genwan-font.git
git clone https://github.com/ButTaiwan/genseki-font
git clone https://github.com/ButTaiwan/gensen-font

# # remove bold style font
rm genseki-font/ttc/GenSekiGothic-{B,H,M,R}.ttc
rm gensen-font/ttc/GenSenRounded-{B,H,M,R}.ttc
rm genwan-font/ttc/GenWanMin-{M,R,SB}.ttc
rm genyo-font/ttc/GenYoMin-{B,H,M,R,SB}.ttc