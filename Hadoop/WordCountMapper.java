import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.StringTokenizer;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;

public class WordCountMapper extends Mapper<LongWritable, Text, Text, LongWritable> {

    private final static LongWritable one = new LongWritable(1);
    private Text word = new Text();

    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {

        Gson gson = new Gson();
        JsonArray jsonArray = gson.fromJson(value.toString(), JsonArray.class);

        for (JsonElement arrayElement : jsonArray) {
            JsonArray array = arrayElement.getAsJsonArray();
            for (JsonElement jsonElement : array) {
                JsonObject jsonObject = jsonElement.getAsJsonObject();

                // Extract the fields you need
                String reviewTitle = jsonObject.get("review_title").getAsString();
//                String rating = jsonObject.get("rating").getAsString();
//                String reviewerAffiliation = jsonObject.get("reviewer_affiliation").getAsString();
//                String jobDate = jsonObject.get("job_date").getAsString();
//                String jobTitle = jsonObject.get("job_title").getAsString();
//                String duration = jsonObject.get("duration").getAsString();
                String pros = jsonObject.get("pros").getAsString();
                String cons = jsonObject.get("cons").getAsString();

                // Tokenize the fields and emit the words with count of 1
                for (String field : new String[]{reviewTitle, pros, cons}) {
                    if (field != null) {
                        StringTokenizer itr = new StringTokenizer(field.toLowerCase());
                        while (itr.hasMoreTokens()) {
                            String cleanedWord = itr.nextToken().replaceAll("^\\p{Punct}+|[\\p{Punct}&&[^']]+$|'(?<!\\w)|(?<!\\w)'", "");
                            if (!cleanedWord.isEmpty()) {
                                word.set(cleanedWord.toLowerCase());
                                context.write(word, one);
                            }
                        }

                    }
                }
            }
        }
    }
}