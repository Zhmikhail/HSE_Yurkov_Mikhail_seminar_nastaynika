

src="$1"
name=tars/$(date +"%Y%m%d_%H%M%S").tar.gz
tar -czf "$name" -C "$(dirname $src)" "basename $src" 2>/dev/null