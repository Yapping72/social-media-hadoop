import java.io.IOException;
import java.util.Date;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;



public class WordCountAnalysis {
	public static void main(String[] args) throws Exception {
		
	Configuration conf = new Configuration();
	Job job = Job.getInstance(conf, "WordCount");
	
	job.setJarByClass(WordCountAnalysis.class);
	
    job.setJarByClass(WordCountAnalysis.class);
    job.setMapperClass(WordCountMapper.class);
    job.setReducerClass(WordCountReducer.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(LongWritable.class);
    //job.setOutputFormatClass(TextOutputFormat.class);
    FileInputFormat.setInputDirRecursive(job, true);
    Path inputPath= new Path("hdfs://hadoop-master:9000/user/ict2102060/Materials/*/*");
    Path outputPath = new Path("hdfs://hadoop-master:9000/user/ict2102060/wordcount/output/");
    
//	Path inputPath = new Path("hdfs://localhost:9000/user/phamvanvung/Materials/WestRock/*");
//	Path outputPath = new Path("hdfs://localhost:9000/user/phamvanvung/wordcount/output/"
//			+ new Date().getTime());//use run-time as output folder
	
	FileInputFormat.addInputPath(job, inputPath);
	FileOutputFormat.setOutputPath(job, outputPath);
	
	System.exit((job.waitForCompletion(true))?0:1);
	}
}