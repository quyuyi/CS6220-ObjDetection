Both Colab notebooks includes the initial experiments done with SSD512 to improve the prediction times.
Both notebooks include the two methods that alternates the fps between 24 fps and one of the selected
fps from following list of fps [5, 10, 15, 20]. First method calculates the cumulative average prediction time
until a specific frame and compares it with the target fps (24 fps). Second method check if there is an increasing
trend in the prediction times in order to alternate the fps.

First notebook, “Methods_Decrease_Prediction_Time.ipynb”, includes the experiments and resulting plots without 
fixing the GPU choice at Google Colab. Second notebook, “Fix_GPU_Methods_Decrease_Prediction_Time.ipynb”, 
includes the experiments and resulting plot after fixing the GPU choice at Colab.

1. Set your file location to object-detection-zoo
2. Run either Fix_GPU_Methods_Decrease_Prediction_Time.ipynb or Methods_Decrease_Prediction_Time.ipynb
3. Install libraries: pip install -r requirements.txt
4. In order to test the methods with different fps, make the following changes to the code cell under “SSD 512” name:
    1. Change the value of “changeTo” variable to one of the selected frame rate from [1/5, 1/10, 1/15, 1/20].
    2. There are two methods in the cell with name “Method 1” and “Method 2”. Comment out the method that is not used.
5. Run the code cells sequentially to obtain results and plots.
