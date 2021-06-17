pipenv run python -m ipykernel install --user --name mygreatenv --display-name "My Great Env"
pipenv run python ./src/Aggregation.py   
cd notebooks
#pipenv run jupyter nbconvert --to notebook --inplace --execute 00_Aggregation.ipynb
pipenv run jupyter nbconvert --to notebook --inplace --execute 01_Preprocessing.ipynb
pipenv run jupyter nbconvert --to notebook --inplace --execute 02_FeedbackGeneration.ipynb
pipenv run jupyter nbconvert --to markdown --TemplateExporter.exclude_input=True 02_FeedbackGeneration.ipynb
mv ./02_FeedbackGeneration_files/02_FeedbackGeneration_6_0.png ../images/heatmap.png
sed 's/^[ \t]*//;s/[ \t]*$//' 02_FeedbackGeneration.md > Readme.md
mv Readme.md ../README.md