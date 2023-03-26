import java.io.IOException;
import java.util.Collections;
import java.util.Map.Entry;
import java.util.TreeMap;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.conf.Configuration;



public class WordCountReducer extends Reducer<Text, LongWritable, Text, LongWritable> {
    private LongWritable totalW = new LongWritable();
    private TreeMap<Long, Text> wordCountMap = new TreeMap<Long, Text>(Collections.reverseOrder());
    private String folderName="";
    
    protected void setup(Context context) throws IOException, InterruptedException {
        Configuration conf = context.getConfiguration();
        folderName = conf.get("folderName");
        Text companyName = new Text(folderName);
        context.write(new Text("Company name: " + companyName+"\n"), null);
        context.write(new Text("Word Count:"), null);

    }

    @Override
    protected void reduce(Text key, Iterable<LongWritable> values,
                          Reducer<Text, LongWritable, Text, LongWritable>.Context context)
            throws IOException, InterruptedException {
        long total = 0;
        for (LongWritable value : values) {
            total += value.get();
        }
        wordCountMap.put(total, new Text(key));
    }

    @Override
    protected void cleanup(Reducer<Text, LongWritable, Text, LongWritable>.Context context)
            throws IOException, InterruptedException {
    	
        // Output only the top 20 most frequent words
        int count = 0;
        for (Entry<Long, Text> entry : wordCountMap.entrySet()) {
            if (count >= 20) {
                break;
            }
            context.write(entry.getValue(), new LongWritable(entry.getKey()));
            count++;
        }
    }
}




