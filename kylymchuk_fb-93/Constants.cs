using System.Text.RegularExpressions;

namespace AAF
{
	public static class Constants
	{
		public static readonly Regex CommandRegex = new(@"([a-zA-Z][a-zA-Z0-9_]+ *)+(\{(\d+,* *)+\})* *;");
		public static readonly Regex IndexNameRegex = new(@"[a-zA-Z][a-zA-Z0-9_]*");
		public static readonly Regex ElementsRegex = new(@"\{(\d+,* *)+\}");
		public static readonly Regex ArgsRegex = new(@"([a-zA-Z0-9_]+|(\{(\d+,* *)+\})+)");
	}
}