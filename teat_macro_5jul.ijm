// Blank ImageJ Macro Script that loops through files in a directory
// Written by Adam Dimech
// https://code.adonline.id.au/imagej-batch-process/

// Specify global variables

input = getDirectory("/Users/maxxim333/Desktop/herrington/05_jul/test_macro");
output = input; // Output images to the same directory as input (prevents second dialogue box, otherwise getDirectory("Output Directory"))

Dialog.create("File Type");
Dialog.addString("File Suffix: ", ".tif", 5); // Select another file format if desired
suffix = Dialog.getString();

processFolder(input);

// Scan folders/subfolders/files to locate files with the correct suffix

function processFolder(input) {
	list = getFileList(input);
	for (i= 1200; i < list.length; i++) {
		if(File.isDirectory(input + list[i]))
			processFolder("" + input + list[i]);
		if(endsWith(list[i], suffix))
			processFile(input, output, list[i]);
	}
}

// Loop through each file

function processFile(input, output, file) {

// Define all variables

MonthNames = newArray("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"); // Generate month names
DayNames = newArray("Sun", "Mon","Tue","Wed","Thu","Fri","Sat"); // Generate date names
getDateAndTime(year, month, dayOfWeek, dayOfMonth, hour, minute, second, msec); // Get date and time information

// Do something to each file
// Disclaimer: Images from H_21_ICC_s08 and H_21_s08 were corrupted so their images are copies from the correspondent H_21 s07 files

open(file);

originalName = getTitle();
if (indexOf(originalName, "ICC") >= 0) {

//run("Brightness/Contrast...");
run("Enhance Contrast", "saturated=0.35");
run("Enhance Contrast", "saturated=0.35");
run("Enhance Contrast", "saturated=0.35");
run("Enhance Contrast", "saturated=0.35");
run("Apply LUT");
run("Despeckle");
saveAs("PNG", "/Users/maxxim333/Desktop/herrington/05_jul/imagej_output/"+originalName+"_cl.png");



close(file);
}
close("*");

// Print log of activities for reference...

print (DayNames[dayOfWeek], dayOfMonth, MonthNames[month], year + "," + hour + ":" + minute + ":" + second + ": Processing " + input + file); 
}

// A final statement to confirm the task is complete...

print("Task complete.");
