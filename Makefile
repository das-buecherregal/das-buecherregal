vue-app-dir = ./interface
vue-assets-dir = ${vue-app-dir}/src/assets
vue-public-dir = ${vue-app-dir}/public

json-copy: texts-meta-copy ruleGroupDefs-copy ruleDefs-copy rule-counts-copy wikipedia-copy

all-copy: analysis-outputs-copy epub-chunks-dir-copy

analysis-outputs-copy: json-copy rules-dir-copy

texts-meta-copy:
	cp ./analysis/texts_meta.json ${vue-assets-dir}

ruleGroupDefs-copy:
	cp ./analysis/ruleGroupDefs.json ${vue-assets-dir}

ruleDefs-copy:
	cp ./analysis/ruleDefs.json ${vue-assets-dir}

rule-counts-copy:
	cp ./analysis/rule_counts.json ${vue-assets-dir}

rules-dir-copy:
	cp -R -v ./analysis/rules ${vue-public-dir} 

wikipedia-copy:
	cp ./analysis/wikipedia.json ${vue-assets-dir}

epub-chunks-dir-copy:
	cp -R -v ./collection/chunks ${vue-public-dir} 
	mv ${vue-public-dir}/chunks ${vue-public-dir}/chunk_epubs

run-identification:
	rm identification/ids.txt
	python3 identification/identification.py

run-collection:
	rm collection/output.json
	rm -rv collection/chunks collection/downloads collection/outputs
	python3 downloader.py
	python3 textify.py
	python3 split_epubs.py

run-analysis:
	rm analysis/*.json
	rm -rv analysis/rules analysis/words
	python3 analysis.py
	python3 author_info.py