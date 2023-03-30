import java.io.IOException;
import java.util.Date;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileStatus;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import java.io.OutputStream;
import java.io.BufferedWriter;
import java.io.OutputStreamWriter;


public class RatingAnalysis {
    public static void main(String[] args) throws Exception {
    	
        // Start timer
        long startTime = System.currentTimeMillis();
        
        // Create a new Configuration object
        Configuration conf = new Configuration();
        // Create a new Job instance
        Job job = Job.getInstance(conf, "RatingCount");
        // Set the Jar file for the job
        job.setJarByClass(RatingAnalysis.class);

        // Set the Mapper and Reducer classes for the job
        job.setMapperClass(RatingCountMapper.class);
        job.setReducerClass(RatingCountReducer.class);

        // Set the output key and value classes for the job
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(LongWritable.class);

        // Set the input and output paths for the job
        Path inputPath = new Path("hdfs://hadoop-master:9000/user/ict2102060/Materials/");
        Path outputPath = new Path("hdfs://hadoop-master:9000/user/ict2102060/ratingcount/output/");
        FileSystem fs = FileSystem.get(conf);
        FileStatus[] status = fs.listStatus(inputPath);

        // Get the name of the input folder
        String folderName = null;
        for (FileStatus s : status) {
            if (s.isDirectory()) {
                folderName = s.getPath().getName();
                break;
            }
        }

        // If the folder name is not null, update the input path and set the folder name in the job configuration
        if (folderName != null) {
            inputPath = new Path("hdfs://hadoop-master:9000/user/ict2102060/Materials/" + folderName + "/*");
            job.getConfiguration().set("folderName", folderName);
        } else {
            // If the folder name is null, set the folder name to "Unknown" in the job configuration
            folderName = "Unknown";
            job.getConfiguration().set("folderName", folderName);
        }

        // Set the input path to be recursive
        FileInputFormat.setInputDirRecursive(job, true);
        // Add the input and output paths to the job
        FileInputFormat.addInputPath(job, inputPath);
        FileOutputFormat.setOutputPath(job, outputPath);

        // Wait for the job to complete and output the time elapsed
        if (job.waitForCompletion(true)) {
            // Get the end time and calculate the elapsed time
            long endTime = System.currentTimeMillis();
            long elapsedTime = (endTime - startTime) / 1000; // in seconds
            
            // Get the output file and append the elapsed time to it
            FileSystem fs2 = FileSystem.get(conf);
            Path outFile = new Path(outputPath, "part-r-00000");
            OutputStream os = fs2.append(outFile);
            BufferedWriter br = new BufferedWriter(new OutputStreamWriter(os));
            br.write("\nElapsed time: " + elapsedTime + " seconds\n");
            br.close();
            System.exit(0);
        } else {
            System.exit(1);
        }
    }
}


