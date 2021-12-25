using System;

namespace AAF
{
	public class Command
	{
		private ArgType[] _argTypes = Array.Empty<ArgType>();
		public Action<string[]> Action { get; private set; }
		private int _minimumArgs;

		public Command(Action<string[]> action)
		{
			Action = action;
		}

		public Command(ArgType[] argTypes, Action<string[]> action) : this(action)
		{
			_argTypes = argTypes;

			_minimumArgs = argTypes.Length;
		}

		public Command(ArgType[] argTypes, int minimumArgs, Action<string[]> action) : this(argTypes, action)
		{
			_minimumArgs = minimumArgs;
		}

		public bool ValidateArgs(string[] args)
		{
			if (args.Length != _argTypes.Length && args.Length < _minimumArgs)
			{
				Console.WriteLine($"Не хватает параметров: {_argTypes.Length - args.Length}!");

				return false;
			}

			for (var i = 0; i < args.Length; i++)
			{
				var regex = _argTypes[i] switch
				{
					ArgType.Name => Constants.IndexNameRegex,
					ArgType.Array => Constants.ElementsRegex,
					_ => Constants.CommandRegex,
				};

				if (!regex.IsMatch(args[i]))
				{
					Console.WriteLine($"Параметр {i+1} имеет неправильный формат!");

					return false;
				}
			}

			return true;
		}
	}
}