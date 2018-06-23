# interview-platform

- Put data directories inside training_data/ folder
- #####To retrain model: 
python retrain.py --bottleneck_dir=tf/bottlenecks --how_many_training_steps=4000 --model_dir=tf/inception/ --summaries_dir=tf/training_summaries/basic --output_graph=tf/retrained_graph.pb --output_labels=tf/retrained_labels.txt --image_dir=training_data/faces

