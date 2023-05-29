# NetMonitor and PlotData User Documentation

## NetMonitor Overview

This NetMonitor is a Python script that conducts two tests regularly:

- A speed test (Download and Upload)
- A ping test

The results of these tests are saved along with a timestamp in a CSV file.

## NetMonitor Usage

To use the tool, execute the script through the command line. You can configure various parameters through the command line:

- `--ping-destination` (`-d`): The destination address for the ping test. The default is `1.1.1.1`.
- `--ping-interval` (`-p`): The interval between ping tests in seconds. The default is 5 seconds.
- `--speedtest-interval` (`-s`): The interval between speed tests in seconds. The default is 3600 seconds (1 hour).
- `--filename` (`-f`): The name of the output file. The default is `network_data.csv`.

For example, if you want to run the tool with a custom ping target address and a custom interval between speed tests, you could use the following command:

```shell
python network_tool.py --ping-destination 8.8.8.8 --speedtest-interval 1800
```

This would run the tool with `8.8.8.8` as the ping target address and an interval of 1800 seconds (30 minutes) between the speed tests.

## NetMonitor Output

The results of the tests are saved in a CSV file, the name of which you can specify when starting the tool. The file has four columns:

- `timestamp`: The time at which the test was conducted.
- `ping_avg`: The average ping time in milliseconds. If the ping test was unsuccessful, this will read "NA".
- `download_speed`: The download speed in Megabits per second. If the speed test was unsuccessful, this will read "NA".
- `upload_speed`: The upload speed in Megabits per second. If the speed test was unsuccessful, this will read "NA".

## NetMonitor Termination

To stop the tool, simply send a `SIGINT` signal (e.g., by pressing `CTRL+C` in the command line where the tool is running). The tool will then stop all ongoing tests and close the output file. Please note that data that was still in the processing queue at the time of receiving the `SIGINT` signal might be lost.

## PlotData Overview

PlotData is a Python script that reads the CSV file generated by the NetMonitor and creates a graphical representation of the network measurement data.

## PlotData Usage

To use the tool, execute the script through the command line. You can configure various parameters through the command line:

- `--input`: Path to the input CSV file. By default, this is `network_data.csv`.
- `--fill_na`: Whether to replace NA values with previous values (forward fill). This is not activated by default.

For example, if you want to run the tool with a custom input file and `fill_na` option, you could use the following command:

```shell
python plotData.py --input custom_data.csv --fill_na
```

This would run the tool with `custom_data.csv` as the input file and the `fill_na` option activated.

## PlotData Output

The output of the tool is a graph with two plots:

- The top plot shows the average ping over time.
- The bottom plot shows the download and upload speed over time.

Each data point in the plots corresponds to a row in the CSV file. The `fill_na` option can be used to replace missing data points with previous values.

## PlotData Termination

Simply close the window to stop the tool. Please note that the generated graph is not automatically saved. To save a copy of the graph, right-click on the graph and select "Save as..." from the context menu.