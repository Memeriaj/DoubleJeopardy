using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Text.RegularExpressions;

namespace GeneticAlgorithm
{
    class Program
    {
        static void Main(string[] args)
        {
            if (args.Count() != 1)
            {
                Console.WriteLine("Requires a single file as input" + args.Count());
                return;
            } 

            #region read file into objects
            Mutant.Candidates = new List<Candidate>();
            using (var inFile = new StreamReader(@"C:\Users\petryjc\Rose-Hulman\AI\Code\Watson\tgmctrain.csv"))
            {
                string line;
                while ((line = inFile.ReadLine()) != null)
                {
                    var fields = line.Split(',').ToList();
                    var newCandidate = new Candidate();
                    newCandidate.CandidateID = Int32.Parse(fields[0]);
                    newCandidate.QuestionID = Convert.ToInt32(double.Parse(fields[1]));
                    newCandidate.FunctionValues = fields.Skip(2).Take(318).Select(e => double.Parse(e)).ToList();
                    newCandidate.Correct = bool.Parse(fields.Last());
                    Mutant.Candidates.Add(newCandidate);
                }
            }
            
            Console.WriteLine("Data set parsed");
            Console.WriteLine("Total " + Mutant.Candidates.Count);
            
            Mutant.PossibleCorrect = Mutant.Candidates.Where(e => e.Correct).Count();
            Console.WriteLine("Possible Correct " + Mutant.PossibleCorrect);
            #endregion

            var mutantList = new List<Mutant>();
            int generationSize = 10;
            int geneticMutants = 0;
            int generationChecks = 200;
            int generations = 10000;
            int g = 0;

            var dataFile = args[0];

            #region read best from previous run
            if (File.Exists(dataFile))
            {
                using (var infile = new StreamReader(dataFile))
                {
                    string line;
                    List<string> buf = new List<string>();
                    while ((line = infile.ReadLine()) != null)
                    {
                        if (line.Contains("Generation"))
                        {
                            buf = new List<string>();
                        }
                        buf.Add(line);
                    }
                    if (buf.Count > 0)
                    {
                        var r1 = new Regex("Generation: (.*)");
                        g = int.Parse(r1.Match(buf[0]).Groups[1].Value);

                        var reg = @"Actual Score: (.*); Number Found: (.*); Genetic Score: .*; Threshhold: (.*); Coeffecients: (.*)";
                        foreach (var l in buf.Skip(1))
                        {
                            var r = new Regex(reg);
                            var m = r.Match(l);
                            var score = m.Groups[1].Value;
                            var found = m.Groups[2].Value;
                            var t = m.Groups[3].Value;
                            var c = m.Groups[4].Value;
                            mutantList.Add(new Mutant(double.Parse(t), c.Split(',').Select(e => double.Parse(e)).ToList(), int.Parse(found), int.Parse(score)));
                        }
                    }
                    
                }
            }

            #endregion
            
            //add enough to make the first generation
            for (int i = mutantList.Count; i < generationSize; i++)
            {
                mutantList.Add(new Mutant());
            }

            for (; g < generations; g++)
            {
                //add in some random children to give extra genetic drift
                for (int i = 0; i < geneticMutants; i++)
                {
                    mutantList.Add(new Mutant());
                }

                //generate child generation
                for (int i = 0; i < generationChecks; i++)
                {
                    mutantList.Add(new Mutant(mutantList[Mutant.r.Next(0, generationSize + geneticMutants)], mutantList[Mutant.r.Next(0, generationSize + geneticMutants)]));
                }

                //select the fittest
                var successorList = new List<Mutant>();

                using (StreamWriter s = new StreamWriter(dataFile, true))
                {
                    Console.WriteLine(string.Format("Generation: {0}", g));
                    s.WriteLine(string.Format("Generation: {0}", g));
                    for (int i = 0; i < generationSize; i++)
                    {
                        var max = mutantList[0];
                        foreach (var scored in mutantList)
                        {
                            if (scored.GeneticScore > max.GeneticScore)
                            {
                                max = scored;
                            }
                        }
                        mutantList.Remove(max);
                        successorList.Add(max);
                        if (i < 20)
                        {
                            Console.WriteLine(max);
                            s.WriteLine(max.DetailedString());
                        }
                    }
                }
                
                mutantList = successorList;
            }
        }
    }
}
