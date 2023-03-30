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


public class RatingCountMapper extends Mapper<LongWritable, Text, Text, LongWritable> {

    // Define a LongWritable object with a value of 1
    private final static LongWritable one = new LongWritable(1);
    // Define a Text object for the rating
    private Text rating = new Text();

    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {

        // Create a Gson object to parse JSON data
        Gson gson = new Gson();
        // Convert the input value (JSON array) to a JsonArray object
        JsonArray jsonArray = gson.fromJson(value.toString(), JsonArray.class);

        // Loop through the JSON array
        for (JsonElement arrayElement : jsonArray) {
            // Convert each element in the array to a new JsonArray object
            JsonArray array = arrayElement.getAsJsonArray();
            // Loop through each element in the new JsonArray
            for (JsonElement jsonElement : array) {
                // Convert each element in the array to a new JsonObject
                JsonObject jsonObject = jsonElement.getAsJsonObject();

                // Extract the value of the "rating" field as a String
                String ratingValue = jsonObject.get("rating").getAsString();

                // Check if the rating is 5.0 or 1.0 and set the Text object accordingly
                if (ratingValue.equals("5.0")) {
                    rating.set("5-star rating");
                } else if (ratingValue.equals("1.0")) {
                    rating.set("1-star rating");
                }

                // Write the rating and the LongWritable object to the context
                context.write(rating, one);
            }
        }
    }
}


