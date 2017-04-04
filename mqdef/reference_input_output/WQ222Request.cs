using System;
using RBFG.Insurance.Framework.DataParsing.Base;


namespace RBFG.Insurance.YJT0.DataParsing
{
	public class WQ222Request : Tran
	{

		public WQ222Request()
		{
			Segments.Add("WQ222Header", new WQ222Header());
			Segments.Add("ActivationStatusRequestList", new ActivationStatusRequestList());
			Segments.Add("MessageEndSegment", new MessageEndSegment());
		}


		public static WQ222Request ToObject(IState state)
		{		
			WQ222Request tran = new WQ222Request();
			WQ222Request result = new WQ222Request();

			int max = tran.Segments.Count;
			for (int i = 0; i < max; i++)
			{
				state = (tran.Segments[i]).ToObject(state);
				result.Segments[i] = state.Output as ISegment;
			}
		
			return result;
		}


		public WQ222Header WQ222Header
		{
			get
			{
				return Segments["WQ222Header"] as WQ222Header;
			}
			set
			{
				WQ222Header = value;
			}
		}

		
		public ActivationStatusRequestList ActivationStatusRequestList
		{
			get
			{
				return Segments["ActivationStatusRequestList"] as ActivationStatusRequestList;
			}
			set
			{
				ActivationStatusRequestList = value;
			}
		}		

		
		public MessageEndSegment MessageEndSegment
		{
			get
			{
				return Segments["MessageEndSegment"] as MessageEndSegment;
			}
			set
			{
				MessageEndSegment = value;
			}
		}		
	}
}