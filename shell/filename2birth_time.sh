for file in *.jpg *.jpeg *.JPG *.png *.PNG; do
	[ -e "$file" ] || continue
	birth_time=$(stat -f %B "$file")
	new_name=$(date -r "$birth_time" +"%Y%m%d_%H%M%S")
	ext="${file##*.}"
	echo "mv $file" "${new_name}.${ext};"
	#mv $file" "${new_name}.${ext}
done
