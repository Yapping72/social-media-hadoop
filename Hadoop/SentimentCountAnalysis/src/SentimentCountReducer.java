import java.io.IOException;
import java.util.Collections;
import java.util.Map.Entry;
import java.util.TreeMap;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.conf.Configuration;


public class SentimentCountReducer extends Reducer<Text, LongWritable, Text, LongWritable> {
    // Initialize a LongWritable variable to store the total word count for a given key.
    private LongWritable totalW = new LongWritable();

    // Initialize a TreeMap to store the word counts for each word.
    private TreeMap<Long, Text> wordCountMap = new TreeMap<Long, Text>(Collections.reverseOrder());

    // Initialize a String variable to store the name of the folder containing the input files.
    private String folderName="";

    // This method runs once at the start of the reducer task and sets up any necessary configuration.
    protected void setup(Context context) throws IOException, InterruptedException {
        Configuration conf = context.getConfiguration();
        // Get the value of the "folderName" configuration variable.
        folderName = conf.get("folderName");
        // Create a new Text object with the folder name and write it to the output with a null value.
        Text companyName = new Text(folderName);
        context.write(new Text("Company name: " + companyName + "\n"), null);
        // Write a message indicating that the word count is about to begin.
        context.write(new Text("Word Count:"), null);
    }

    // This method is called for each key-value pair in the input.
    @Override
    protected void reduce(Text key, Iterable<LongWritable> values,
                          Reducer<Text, LongWritable, Text, LongWritable>.Context context)
            throws IOException, InterruptedException {
        // Initialize a long variable to store the total count for the current key.
        long total = 0;
        // Loop through the values and add them to the total.
        for (LongWritable value : values) {
            total += value.get();
        }
        // Add the word count to the TreeMap.
        wordCountMap.put(total, new Text(key));
    }

    // This method runs once at the end of the reducer task and outputs the final result.
    @Override
    protected void cleanup(Reducer<Text, LongWritable, Text, LongWritable>.Context context)
            throws IOException, InterruptedException {
        for (Entry<Long, Text> entry : wordCountMap.entrySet()) {
            // Write a key-value pair to the output with the word as the key and the count as the value.
            context.write(entry.getValue(), new LongWritable(entry.getKey()));
        }
    }

}
