import java.io.IOException;
import java.util.Arrays;
import java.util.List;
import java.util.StringTokenizer;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;


public class WordCountMapper extends Mapper<LongWritable, Text, Text, LongWritable> {

    private final static LongWritable one = new LongWritable(1);
    private Text word = new Text();

    private final static List<String> FILLER_WORDS = Arrays.asList("too","much","are","can","get","have","very","if","be","a", "an", "the", "and", "as", "at", "but", "by", "for", "from", "in", "into", "is", "it", "no", "not", "of", "on", "or", "such", "that", "the", "their", "then", "there", "these", "they", "this", "to", "was", "will", "with", "i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "them", "my", "mine", "your", "yours", "his", "her", "hers", "its", "ours", "theirs", "that", "which", "who", "whom", "whose", "what", "where", "when", "why", "how", "all", "any", "both", "each", "few", "more", "most", "neither", "none", "other", "some", "such");

    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {

        Gson gson = new Gson();
        JsonArray jsonArray = gson.fromJson(value.toString(), JsonArray.class);

        for (JsonElement arrayElement : jsonArray) {
            JsonArray array = arrayElement.getAsJsonArray();
            for (JsonElement jsonElement : array) {
                JsonObject jsonObject = jsonElement.getAsJsonObject();

                // Extract the fields you need
                String reviewTitle = jsonObject.get("review_title").getAsString();
                String pros = jsonObject.get("pros").getAsString();
                String cons = jsonObject.get("cons").getAsString();

                // Tokenize the fields and emit the words with count of 1
                for (String field : new String[]{reviewTitle, pros, cons}) {
                    if (field != null) {
                        StringTokenizer itr = new StringTokenizer(field.toLowerCase());
                        while (itr.hasMoreTokens()) {
                            String cleanedWord = itr.nextToken().replaceAll("^\\p{Punct}+|[\\p{Punct}&&[^']]+$|'(?<!\\w)|(?<!\\w)'", "");
                            if (!cleanedWord.isEmpty() && !FILLER_WORDS.contains(cleanedWord)) {
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
