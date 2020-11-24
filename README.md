## Environment Setup
Create virtual environment for both Python and Javascript.
```
./bin/objdectInstall
```

## Run the app
Compile the JS code, and launch the backend server,
```
$ ./bin/objdectRun
```
Navigate to `localhost:8000`



## Colab for frame skipping in the setting of combining boosting tracker and YOLO MobileNet (optional as we later convert the jupternotebook into local one)

(0) The base of the code is from https://github.com/khchow-gt/object-detection-zoo & https://www.dropbox.com/s/vhhnp3wt4oztkqz/model_weights.zip?dl=0

(1) download all the files in this google drive [https://drive.google.com/drive/folders/1mR1U6gVOxfXT8w__yRZB-nsBTibKDh8G?usp=sharing] link to your google drive.

(2) run demo_v1_1.ipynb. First, mount your system to your drive. Second, pip install the packages in the code segment. Third, restart Runtime.

(3) Run the left code blocks sequentially until second last block. Go to output directory and create a directory yolov3mobile${fps}  (e.g. yolov3mobile10)

(4) In the last block, set the fps you want and then run it.

(5) The results will be in output/yolov3mobile{fps} directory in your google drive.
