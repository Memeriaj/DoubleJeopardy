using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace GeneticAlgorithm
{
    class Mutant
    {
        public static Random r = new Random();
        //All of the potential candidates
        public static List<Candidate> Candidates { get; set; }

        //The threshhold above which answers are considered to pass
        public double Threshhold { get; set; }
        //Coeffecients of the linear function defining the value of the functions
        public List<double> Coeffecients { get; set; }

        private int? numberFound;
        public int NumberFound
        {
            get
            {
                if (numberFound == null)
                {
                    Score();
                }
                return numberFound ?? 0;
            }
        }

        private int? actualScore;
        public int ActualScore
        {
            get
            {
                if (actualScore == null)
                {
                    Score();
                }
                return actualScore ?? Int32.MinValue;
            }
        }

        public static int PossibleCorrect { get; set; }
        public static int PossibleTotal { get { return Mutant.Candidates.Count;  } }

        public double GeneticScore
        {
            get 
            {
                var numberMissed = ActualScore - NumberFound;
                return NumberFound/(double)PossibleCorrect + numberMissed/(double)PossibleTotal;
            }
        }

        /// <summary>
        /// Creates a new random mutant
        /// </summary>
        public Mutant()
        {
            Coeffecients = new List<double>();
            Threshhold = r.Next(-10, 10);
            for (int i = 0; i < Candidate.FunctionValueCount; i++)
            {
                Coeffecients.Add(200 * (r.NextDouble() - 0.5));
            }
        }

        public Mutant(double t, List<double> c, int numFound, int score)
        {
            Coeffecients = c;
            Threshhold = t;
            numberFound = numFound;
            actualScore = score;
        }

        /// <summary>
        /// Creates a new mutant from two mutants with some genetic mutation
        /// </summary>
        /// <param name="m1">1 parents</param>
        /// <param name="m2">Second parent</param>
        public Mutant(Mutant m1, Mutant m2)
        {
            Coeffecients = new List<double>();
            Threshhold = PickSuccessor(m1.Threshhold, m2.Threshhold, 0.2, 1000);
            for (int i = 0; i < Candidate.FunctionValueCount; i++)
            {
                Coeffecients.Add(PickSuccessor(m1.Coeffecients[i], m2.Coeffecients[i], 0.3, 7));
            }
        }

        private double PickSuccessor(double p1, double p2, double mutationRate, double mutationVariance)
        {
            var o = r.NextDouble();
            if (o > mutationRate / 2)
            {
                return p1 + mutationVariance * 2 * (r.NextDouble() - 0.5);
            }
            else if (o < mutationRate)
            {
                return p2 + mutationVariance * 2 * (r.NextDouble() - 0.5);
            }
            else if (o < 0.5 + mutationRate / 2)
            {
                return p1;
            }
            else
            {
                return p2;
            }
        }

        /// <summary>
        /// returns the score of the candidates using the present mutant
        /// </summary>
        /// <param name="scale">Alters the importance of getting correct (as opposed to not getting wrong) answers</param>
        /// <returns>the score</returns>
        private void Score()
        {
            actualScore = 0;
            numberFound = 0;

            foreach (var candidate in Candidates)
            {
                var evaluation = Evaluation(candidate);
                if (evaluation > Threshhold)
                {
                    actualScore += candidate.Correct ? 1 : -1;
                    numberFound += candidate.Correct ? 1 : 0;
                }
            }

            
        }

        /// <summary>
        /// Returns the linear combination of the function values and the candidate answers
        /// </summary>
        /// <param name="candidate">Any givin candidate answer</param>
        /// <returns>A double representing the linear combination</returns>
        private double Evaluation(Candidate candidate)
        {
            var total = 0.0;
            for (int i = 0; i < Candidate.FunctionValueCount; i++)
            {
                total += candidate.FunctionValues[i] * Coeffecients[i];
            }
            return total;
        }

        public override string ToString()
        {
            return string.Format("Score: {0}; Number Found: {1}; Genetic Score: {2}",
                ActualScore, NumberFound, GeneticScore);
        }

        public string DetailedString()
        {
            return string.Format("Actual Score: {0}; Number Found: {1}; Genetic Score: {2}; Threshhold: {3}; Coeffecients: {4}",
                ActualScore, NumberFound, GeneticScore, Threshhold, string.Join(",", Coeffecients));
        }
    }
}
