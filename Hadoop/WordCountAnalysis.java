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

public class WordCountAnalysis {
    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "WordCount");
        job.setJarByClass(WordCountAnalysis.class);

        job.setMapperClass(WordCountMapper.class);
        job.setReducerClass(WordCountReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(LongWritable.class);

        Path inputPath = new Path("hdfs://hadoop-master:9000/user/ict2102060/Materials/");
        Path outputPath = new Path("hdfs://hadoop-master:9000/user/ict2102060/wordcount/output/");
        FileSystem fs = FileSystem.get(conf);
        FileStatus[] status = fs.listStatus(inputPath);

        String folderName = null;
        for (FileStatus s : status) {
            if (s.isDirectory()) {
                folderName = s.getPath().getName();
                break;
            }
        }

        if (folderName != null) {
            inputPath = new Path("hdfs://hadoop-master:9000/user/ict2102060/Materials/" + folderName + "/*");
            job.getConfiguration().set("folderName", folderName);
        } else {
            folderName = "Unknown";
            job.getConfiguration().set("folderName", folderName);
        }

        FileInputFormat.setInputDirRecursive(job, true);
        FileInputFormat.addInputPath(job, inputPath);
        FileOutputFormat.setOutputPath(job, outputPath);

        System.exit((job.waitForCompletion(true)) ? 0 : 1);
    }
}
