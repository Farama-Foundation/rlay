#!/bin/bash

# Prompt the user to enter a package name
echo "Please enter a package name:"
read package_name


package_name_capitalized="$(echo "${package_name:0:1}" | tr '[:lower:]' '[:upper:]')${package_name:1}"

# Rename the current directory from 'rlay' to the given package name
if [ "$(basename "$(pwd)")" == "rlay" ]; then
    cd ..
    mv rlay "$package_name"
    cd "$package_name"
else
    echo "Error: The current directory must be named 'rlay'"
    exit 1
fi

# Replace all instances of 'rlay' or 'Rlay' with the new package name

#find "rlay" -type f -exec perl -i -pe "s/Rlay/${package_name_capitalized}/g; s/rlay/${package_name}/g" {} \;
#find . -type f -exec sed -i 's/rlay/ferry/g' {} +

find . -type f -exec sed -i.bak "s/rlay/${package_name}/g" {} +
find . -type f -exec sed -i.bak "s/Rlay/${package_name_capitalized}/g" {} +
find . -type f -name "*.bak" -delete


mv rlay "$package_name"

# Check if the current directory has a git repository
if [ -d ".git" ]; then
    # Delete the existing git repository
    rm -rf .git
    echo "Existing git repository deleted"
fi

# Initialize a new git repository with the current contents
git init
echo "New git repository initialized"

# Add all the files and commit the changes
git add .
git commit -m "Initial commit after renaming project to $package_name"

echo "Directory and file contents have been updated, and a new git repository has been initialized"

script_path=$(realpath "$0")

# Remove the script file
rm "$script_path"

echo "The script commited sudoku and has removed itself"

echo ""
echo "Remember to execute the following command to work in the renamed directory"
echo "cd ../${package_name}"