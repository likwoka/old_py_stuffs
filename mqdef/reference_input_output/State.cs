using System;
using RBFG.Insurance.Framework.DataParsing.Base;


namespace RBFG.Insurance.YJT0.DataParsing
{

	public class State : IState
	{
		public State(string input, int startPos)
		{
			_input = input;
			_startPos = startPos;
		}


		public State(string input) : this(input, 0) {}


		public string Input
		{
			get
			{
				return _input;
			}
			set
			{
				_input = value;
			}
		}


		public object Output
		{
			get
			{
				return _output;
			}
			set
			{
				_output = value;
			}
		}


		public int StartPos
		{
			get
			{
				return _startPos;
			}
			set
			{
				_startPos = value;
			}
		}


		private string _input;
		private int _startPos;
		private object _output;
	}
}
