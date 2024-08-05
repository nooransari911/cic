# exec ssh-agent bash
# ssh-add ~/.ssh/github_key_1


ssh -T git@github.com
git add .gitignore
git add .
# git remote add origin https://github.com/nooransari911/cic.git
git remote set-url origin git@github.com:nooransari911/cic.git
echo "Enter commit message:"
read commit_message
echo ""
echo "Starting commit;"
git commit -m "$commit_message"
echo ""
echo "Starting push;"
git push -u origin main
