pipenv run python -m ipykernel install --user --name mygreatenv --display-name "My Great Env"
pipenv run python ./src/Aggregation.py   
cd notebooks
#pipenv run jupyter nbconvert --to notebook --inplace --execute 00_Aggregation.ipynb
pipenv jupyter nbconvert --to notebook --inplace --execute 01_Preprocessing.ipynb
pipenv jupyter nbconvert --to notebook --inplace --execute 02_FeedbackGeneration.ipynb
pipenv jupyter nbconvert --to markdown --TemplateExporter.exclude_input=True 02_FeedbackGeneration.ipynb
sed "s/02_FeedbackGeneration_files/notebooks\/02_FeedbackGeneration_file/g" 02_FeedbackGeneration.md > output.md
sed 's/^[ \t]*//;s/[ \t]*$//' output.md > Readme.md
mv Readme.md ../README.md
