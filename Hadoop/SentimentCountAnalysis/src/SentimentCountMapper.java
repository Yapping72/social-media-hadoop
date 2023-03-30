import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.StringTokenizer;
import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;





public class SentimentCountMapper extends Mapper<LongWritable, Text, Text, LongWritable> {

    // Initialize a LongWritable object with a value of 1 for counting
    private final static LongWritable one = new LongWritable(1);
    
    private final static List<String> FILLER_WORDS = Arrays.asList("too","much","are","can","get","have","very","if","be","a", "an", "the", "and", "as", "at", "but", "by", "for", "from", "in", "into", "is", "it", "no", "not", "of", "on", "or", "such", "that", "the", "their", "then", "there", "these", "they", "this", "to", "was", "will", "with", "i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "them", "my", "mine", "your", "yours", "his", "her", "hers", "its", "ours", "theirs", "that", "which", "who", "whom", "whose", "what", "where", "when", "why", "how", "all", "any", "both", "each", "few", "more", "most", "neither", "none", "other", "some", "such");


    // Initialize a Text object for storing the word being counted
    private Text emotion = new Text();

    // Initialize a HashMap for mapping words to their corresponding emotions
    private HashMap<String, String> wordToEmotion = new HashMap<>();

    // The setup function for loading the word and emotion list
    @Override
    protected void setup(Context context) throws IOException, InterruptedException {
        // Initialize a HashMap for storing the word and emotion list
        HashMap<String, ArrayList<String>> df = new HashMap<>();

        // Read words from words.json
        InputStream wordStream = SentimentCountMapper.class.getClassLoader().getResourceAsStream("words.json");
        BufferedReader wordReader = new BufferedReader(new InputStreamReader(wordStream));
        String wordLine = wordReader.readLine();
        Gson gson = new Gson();
        JsonObject wordJson = gson.fromJson(wordLine, JsonObject.class);
        JsonArray wordArray = wordJson.getAsJsonArray("Words");
        ArrayList<String> wordList = new ArrayList<>();
        for (JsonElement wordElement : wordArray) {
            String word = wordElement.getAsString();
            wordList.add(word);
        }
        df.put("Word", wordList);
        wordReader.close();

        // Read emotions from emotions.json
        InputStream emotionStream = SentimentCountMapper.class.getClassLoader().getResourceAsStream("emotions.json");
        BufferedReader emotionReader = new BufferedReader(new InputStreamReader(emotionStream));
        String emotionLine = emotionReader.readLine();
        JsonObject emotionJson = gson.fromJson(emotionLine, JsonObject.class);
        JsonArray emotionArray = emotionJson.getAsJsonArray("Emotions");
        ArrayList<String> emotionList = new ArrayList<>();
        for (JsonElement emotionElement : emotionArray) {
            String emotion = emotionElement.getAsString();
            emotionList.add(emotion);
        }
        df.put("Emotion", emotionList);
        emotionReader.close();

        // Initialize a HashMap for mapping words to their corresponding emotions
        wordToEmotion = new HashMap<>();
        ArrayList<String> words = df.get("Word");
        ArrayList<String> emotions = df.get("Emotion");
        for (int i = 0; i < words.size(); i++) {
            String word = words.get(i);
            String emotion = emotions.get(i);
            wordToEmotion.put(word.toLowerCase(), emotion);
        }
    }





    // The map function
    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {

        // Convert the JSON string input to a JSON array
        Gson gson = new Gson();
        JsonArray jsonArray = gson.fromJson(value.toString(), JsonArray.class);

        // Iterate through each element in the JSON array
        for (JsonElement arrayElement : jsonArray) {

            // Convert the array element to a JSON array and iterate through each element in it
            JsonArray array = arrayElement.getAsJsonArray();
            for (JsonElement jsonElement : array) {

                // Convert the array element to a JSON object
                JsonObject jsonObject = jsonElement.getAsJsonObject();

                // Extract the fields you need
                String reviewTitle = jsonObject.get("review_title").getAsString();
                String pros = jsonObject.get("pros").getAsString();
                String cons = jsonObject.get("cons").getAsString();

                // Tokenize the fields and emit the emotions with count of 1
                for (String field : new String[]{reviewTitle, pros, cons}) {
                    if (field != null) {
                        // Tokenize the field and remove punctuation and filler words
                        StringTokenizer itr = new StringTokenizer(field.toLowerCase());
                        while (itr.hasMoreTokens()) {
                            String cleanedWord = itr.nextToken().replaceAll("^\\p{Punct}+|[\\p{Punct}&&[^']]+$|'(?<!\\w)|(?<!\\w)'", "");
                            if (!cleanedWord.isEmpty()&& !FILLER_WORDS.contains(cleanedWord)) {
                                // Get the corresponding emotion for the word and emit it with a count of 1
                                String emotionStr = wordToEmotion.get(cleanedWord);
                                if (emotionStr != null) {
                                    emotion.set(emotionStr);
                                    context.write(emotion, one);
                                }
                            }
                         }
                     }
                  }
           }
         }
     }
 }


