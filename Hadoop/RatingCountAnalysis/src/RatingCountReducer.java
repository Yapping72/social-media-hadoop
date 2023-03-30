import java.io.IOException;
import java.util.Collections;
import java.util.Map.Entry;
import java.util.TreeMap;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.conf.Configuration;


public class RatingCountReducer extends Reducer<Text, LongWritable, Text, LongWritable> {
    private LongWritable totalW = new LongWritable();
    private String folderName="";

    // This method is called once at the start of the reduce task.
    // It retrieves the name of the input folder from the configuration,
    // and writes it and the header text for the rating count to the output.
    protected void setup(Context context) throws IOException, InterruptedException {
        Configuration conf = context.getConfiguration();
        folderName = conf.get("folderName");
        Text companyName = new Text(folderName);
        context.write(new Text("Company name: " + companyName+"\n"), null);
        context.write(new Text("Rating Count:"), null);
    }

    // This method is called once for each key in the input data set.
    // It sums the values for each key (which represents a rating), and writes
    // the total count for that rating to the output.
    @Override
    protected void reduce(Text key, Iterable<LongWritable> values,
                          Reducer<Text, LongWritable, Text, LongWritable>.Context context)
            throws IOException, InterruptedException {
        long total = 0;
        for (LongWritable value : values) {
            total += value.get();
        }
        context.write(key, new LongWritable(total));
    }
}
