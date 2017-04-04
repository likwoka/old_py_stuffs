using System;
using RBFG.Insurance.Framework.DataParsing.Base;


namespace RBFG.Insurance.YJT0.DataParsing
{

	public class ActivationStatusRequestList : SegmentList
	{
		
		public ActivationStatusRequest this[int index]
		{
			get
			{
				return List[index] as ActivationStatusRequest;
			}
			set
			{
				List[index] = value;
			}
		}


		public override IState ToObject(IState state)
		{	
			Segment segment = new ActivationStatusRequest();
			string input = state.Input;
			int pos = state.StartPos;
			int end = input.Length;
			int length = segment.Fields[0].Length;
			
			while (pos < end)
			{
				string label = input.Substring(pos, length);
				
				if (segment.Fields[0].String == label)
				{
					segment = new ActivationStatusRequest();
					state = segment.ToObject(state);
					List.Add(state.Output);
					pos = state.StartPos;
				}
				else
				{
					break;
				}
			}
			
			state.Output = this;			
			return state;
		}
	}
}
