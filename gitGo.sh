if [ $1 = "push" ]; then
    git add .
    # commit 写入时间
    git commit -m "$(date +'%Y-%m-%d %H:%M:%S')"
    git push
fi

if [ $1 = "pull" ]; then
    git pull
fi