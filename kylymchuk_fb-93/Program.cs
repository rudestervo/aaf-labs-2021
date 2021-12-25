using System;
using System.Collections.Generic;
using System.Linq;

namespace AAF
{
	class Program
	{
		private const string CommandExit = "exit";
		private const string CommandCreate = "create";
		private const string CommandInsert = "insert";
		private const string CommandPrint = "print_index";
		private const string CommandContains = "contains";
		private const string CommandSearch = "search";

		private const string SearchWhere = "where";
		private const string SearchIntersects = "intersects";
		private const string SearchContains = "contains";
		private const string SearchContainedBy = "contained_by";

		private static readonly Dictionary<string, int> Indexes = new();
		private static readonly Dictionary<string, Dictionary<int, List<int>>> Database = new();

		private static readonly Dictionary<string, Command> Commands = new()
		{
			{ CommandExit, new Command(Exit) },
			{ CommandCreate, new Command(new[] { ArgType.Name }, Create) },
			{ CommandInsert, new Command(new[] { ArgType.Name, ArgType.Array }, Insert) },
			{ CommandPrint, new Command(new[] { ArgType.Name }, Print) },
			{ CommandContains, new Command(new[] { ArgType.Name, ArgType.Array }, Contains) },
			{
				CommandSearch,
				new Command(new[] { ArgType.Name, ArgType.Name, ArgType.Name, ArgType.Array }, 1, Search)
			},
		};

		private static void Main()
		{
			// ProcessCommand("CREATE grades;");
			// ProcessCommand("CREATE grades;");
			// ProcessCommand("INSERT grades2 {1, 2, 3};");
			// ProcessCommand("INSERT grades {1, 2, 3};");
			// ProcessCommand("INSERT grades {4, 6};");
			// ProcessCommand("INSERT grades {1, 4};");
			// ProcessCommand("print_index grades;");
			// ProcessCommand("contains grades {1, 2};");
			// ProcessCommand("contains grades {1, 2, 3};");
			// ProcessCommand("search grades;");
			// ProcessCommand("SEARCH grades WHERE INTERSECTS {4, 90};");
			// ProcessCommand("SEARCH grades WHERE CONTAINS {1, 2};");
			// ProcessCommand("SEARCH grades WHERE CONTAINED_BY {1, 2, 3, 4, 5};");

			var buffer = "";
			while (true)
			{
				var input = Console.ReadLine() ?? "";

				buffer += $" {input}";

				if (!input.Contains(";"))
				{
					continue;
				}

				ProcessCommand(buffer);

				buffer = "";
			}
		}

		private static void ProcessCommand(string input)
		{
			input = input.Split(separator: ";")[0] + ";";
			
			if (!Constants.CommandRegex.IsMatch(input))
			{
				Console.WriteLine("Неверный синтаксис!");

				return;
			}
			
			var args = Constants.ArgsRegex.Matches(input).Select(m => m.Value).ToArray();
			
			Console.WriteLine(string.Join(" ", args));
			
			args[0] = args[0].ToLower();

			if (!Commands.ContainsKey(args[0]))
			{
				Console.WriteLine($"Неизвестная команда: {args[0]}");

				return;
			}

			var command = Commands[args[0]];
			args = args.Length > 1 ? args[1..] : Array.Empty<string>();

			if (command.ValidateArgs(args))
			{
				try
				{
					command.Action.Invoke(args);
				}
				catch
				{
					Console.WriteLine("Произошла ошибка, проверьте правильность написания команды.");
				}
			}

			Console.WriteLine("----------------------");
		}

		private static void Exit(string[] args)
		{
			Environment.Exit(0);
		}

		private static void Create(string[] args)
		{
			var name = args[0];

			if (Database.ContainsKey(name))
			{
				Console.WriteLine($"Коллекция {name} уже существует");

				return;
			}

			Database.Add(name, new Dictionary<int, List<int>>());
			Indexes.Add(name, 1);

			Console.WriteLine($"Коллекция {name} была успешно создана.");
		}

		private static void Insert(string[] args)
		{
			var name = args[0];
			var elements = ParseElements(args[1]);

			foreach (var element in elements)
			{
				if (!Database[name].ContainsKey(element))
				{
					Database[name].Add(element, new List<int>());
				}

				Database[name][element].Add(Indexes[name]);
			}

			Indexes[name]++;

			Console.WriteLine($"Значения успешно добавлены в коллекцию {name}");
		}

		private static void Print(string[] args)
		{
			var name = args[0];

			foreach (var (value, indexes) in Database[name].OrderBy(pair => pair.Key))
			{
				Console.WriteLine($"{value}: {string.Join(", ", indexes)}");
			}
		}

		private static void Contains(string[] args)
		{
			var name = args[0];
			var elements = ParseElements(args[1]);
			var count = elements.Count;

			var result = ContainsElements(name, elements);

			if (result == null)
			{
				Console.WriteLine(false);

				return;
			}

			Console.WriteLine(result.Any(value => Database[name].Count(pair => pair.Value.Contains(value)) == count));
		}

		private static void Search(string[] args)
		{
			var name = args[0];

			if (args.Length == 1)
			{
				for (var i = 1; i < Indexes[name]; i++)
				{
					PrintIndex(name, i);
				}
			}
			else
			{
				if (args[1].ToLower() != SearchWhere)
				{
					Console.WriteLine("Не хватает ключевого слова \"WHERE\"!");

					return;
				}

				var elements = ParseElements(args[3]);

				var indexes = new HashSet<int>();
				switch (args[2].ToLower())
				{
					case SearchIntersects:
						foreach (var i in elements
							.Where(element => Database[name].ContainsKey(element))
							.SelectMany(element => Database[name][element]))
						{
							indexes.Add(i);
						}

						break;
					case SearchContains:
						indexes = ContainsElements(name, elements).ToHashSet();

						break;
					case SearchContainedBy:
						for (var i = 1; i < Indexes[name]; i++)
						{
							var result = Database[name]
								.Where(pair => pair.Value.Contains(i))
								.Select(pair => pair.Key)
								.ToList();

							if (result.Count > 0 && result.TrueForAll(e => elements.Contains(e)))
							{
								indexes.Add(i);
							}
						}

						break;
					default:
						Console.WriteLine($"Неправильная команда для поиска: {args[2]}!");
						break;
				}

				PrintIndexes(name, indexes.ToArray());
			}
		}

		private static List<int> ContainsElements(string name, List<int> elements)
		{
			var firstElement = elements[0];
			elements.RemoveAt(0);

			if (!Database[name].ContainsKey(firstElement))
			{
				return null;
			}

			var buffer = Database[name][firstElement];

			while (elements.Count > 0)
			{
				var value = elements[0];

				if (!Database[name].ContainsKey(value))
				{
					return null;
				}

				buffer = buffer.Intersect(Database[name][value]).ToList();

				if (buffer.Count == 0)
				{
					return null;
				}

				elements.RemoveAt(0);
			}

			return buffer;
		}

		private static void PrintIndexes(string name, int[] indexes)
		{
			foreach (var i in indexes)
			{
				PrintIndex(name, i);
			}
		}

		private static void PrintIndex(string name, int index)
		{
			var result = Database[name]
				.Where(pair => pair.Value.Contains(index))
				.Select(pair => pair.Key)
				.ToList();

			if (result.Count > 0)
			{
				Console.WriteLine($"{index}: {{{string.Join(", ", result)}}}");
			}
		}

		private static List<int> ParseElements(string row)
		{
			return row
				.Replace("{", "")
				.Replace("}", "")
				.Split(",")
				.Select(e => Convert.ToInt32(e))
				.ToList();
		}
	}
}