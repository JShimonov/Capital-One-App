export SECRET_KEY="990b28a2434e2529815bbc1674ca8a45e94270939d769515"
export DEBUG_VALUE="True"

for file in ~/.{bash_prompt, aliases, private}; do
	[ -r "$file" ] && [ -f "$file" ] && source "$file";
done;

