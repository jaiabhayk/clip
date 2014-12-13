/**
 * 
 */
package clip;

/**
 * @author JaiAbhay
 *
 */
public class Tweet {

	private String oldId;
	private String newId;
	private float oldScore;
	private float newScore;
	private String tweet;

	/**
	 * @return the oldScore
	 */
	public float getOldScore() {
		return oldScore;
	}

	/**
	 * @param oldScore
	 *            the oldScore to set
	 */
	public void setOldScore(float oldScore) {
		this.oldScore = oldScore;
	}

	public static String TAB = "	";

	public Tweet(String line) throws Exception {
		System.out.println(line);
		String[] tokens = line.split(TAB);

		if (tokens.length == 4) {
			oldId = tokens[0].trim();
			newId = tokens[1].trim();
			oldScore = Float.valueOf(tokens[2].trim());
			newScore = oldScore;
			tweet = tokens[3];
		} else if (tokens.length == 3) {
			oldId = tokens[0].trim();
			newId = oldId;
			oldScore = Float.valueOf(tokens[1].trim());
			newScore = oldScore;
			tweet = tokens[2];
		} else {
			throw new Exception("Unexpected format of the tweet");
		}

	}

	public Tweet(Tweet trainTweet) {
		oldId = trainTweet.getOldId();
		newId = trainTweet.getNewId();

		oldScore = trainTweet.getOldScore();
		newScore = trainTweet.getNewScore();
		tweet = trainTweet.getTweet();

	}

	/**
	 * @return the oldId
	 */
	public String getOldId() {
		return oldId;
	}

	/**
	 * @param oldId
	 *            the oldId to set
	 */
	public void setOldId(String oldId) {
		this.oldId = oldId;
	}

	/**
	 * @return the newId
	 */
	public String getNewId() {
		return newId;
	}

	/**
	 * @param newId
	 *            the newId to set
	 */
	public void setNewId(String newId) {
		this.newId = newId;
	}

	/**
	 * @return the score
	 */
	public float getScore() {
		return oldScore;
	}

	/**
	 * @param score
	 *            the score to set
	 */
	public void setScore(float score) {
		this.oldScore = score;
	}

	/**
	 * @return the tweet
	 */
	public String getTweet() {
		return tweet;
	}

	/**
	 * @param tweet
	 *            the tweet to set
	 */
	public void setTweet(String tweet) {
		this.tweet = tweet;
	}

	@Override
	public String toString() {
		return String.valueOf(newId) + TAB
				+ String.valueOf(newScore) + TAB + tweet;

	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see java.lang.Object#hashCode()
	 */
	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + ((oldId == null) ? 0 : oldId.hashCode());
		return result;
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see java.lang.Object#equals(java.lang.Object)
	 */
	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		Tweet other = (Tweet) obj;
		if (oldId == null) {
			if (other.oldId != null)
				return false;
		} else if (!oldId.equals(other.oldId))
			return false;
		return true;
	}

	/**
	 * @return the newScore
	 */
	public float getNewScore() {
		return newScore;
	}

	/**
	 * @param newScore
	 *            the newScore to set
	 */
	public void setNewScore(float newScore) {
		this.newScore = newScore;
	}

	public static Tweet mergeTweets(Tweet trainTweet, Tweet testTweet) {
		Tweet t = new Tweet(trainTweet);
		float score = (testTweet.getOldScore() + trainTweet.getOldScore())/2;
		t.setOldScore(score);
		t.setNewScore(score);
		return t;
	}

}
