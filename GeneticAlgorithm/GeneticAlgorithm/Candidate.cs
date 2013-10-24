using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace GeneticAlgorithm
{
    class Candidate
    {
        public static int FunctionValueCount = 318;
        public int QuestionID { get; set; }
        public int CandidateID { get; set; }
        public bool Correct { get; set; }
        public List<double> FunctionValues { get; set; }
    }
}
