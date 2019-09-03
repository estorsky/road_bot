#!/bin/bash
# Перекодирует рекурсивно в текущем каталоге имена
# файлов и каталогов в транслит.

shopt -s nullglob
for NAME in * ; do
TRS=$(echo $NAME | sed "y/абвгдезийклмнопрстуфхц/abvgdezijklmnoprstufxc/")
TRS=$(echo $TRS | sed "y/АБВГДЕЗИЙКЛМНОПРСТУФХЦ/ABVGDEZIJKLMNOPRSTUFXC/")
TRS=${TRS//ч/ch} TRS=${TRS//Ч/CH};
TRS=${TRS//ш/sh} TRS=${TRS//Ш/SH};
TRS=${TRS//ё/jo} TRS=${TRS//Ё/JO};
TRS=${TRS//ж/zh} TRS=${TRS//Ж/ZH};
TRS=${TRS//щ/shh} TRS=${TRS//Щ/SHH};
TRS=${TRS//э/e} TRS=${TRS//Э/E};
TRS=${TRS//ю/ju} TRS=${TRS//Ю/JU};
TRS=${TRS//я/ja} TRS=${TRS//Я/JA};
TRS=${TRS//ъ/} TRS=${TRS//Ъ/};
TRS=${TRS//ь/} TRS=${TRS//Ь/};
TRS=${TRS//ы/y} TRS=${TRS//Ы/Y};

TRS=${TRS//«/} TRS=${TRS//»/};

if [[ $(file -b "$NAME") == directory ]]; then
mv -v "$NAME" "$TRS"
cd "$TRS"
"$0"
cd ..
else
mv -v "$NAME" "$TRS"
fi
done

